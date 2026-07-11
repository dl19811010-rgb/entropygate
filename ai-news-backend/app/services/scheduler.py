"""Scheduler — Priority-based dynamic scheduling with Editorial Calendar support.

Replaces the old tier-based fixed-interval scheduler with a priority-driven model:
  critical → 5 min, high → 15 min, normal → 30 min, low → 120 min

During active Editorial Calendar events, source priorities are boosted automatically.
"""
import logging
from datetime import datetime
from typing import Optional, List

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger

from app.core.editorial_policy import PRIORITY_SCHEDULE, get_effective_priority, get_effective_interval

logger = logging.getLogger(__name__)


class SchedulerService:
    def __init__(self, db=None):
        self.db = db
        self.scheduler = None
        self._running = False

    def start(self):
        if self._running:
            logger.info("Scheduler already running")
            return

        logger.info("Starting priority-based crawl scheduler...")

        self.scheduler = BackgroundScheduler(timezone="UTC")

        # ── One job per priority level
        for priority, config in PRIORITY_SCHEDULE.items():
            self.scheduler.add_job(
                self._crawl_by_priority,
                args=[priority],
                trigger=IntervalTrigger(minutes=config["interval_minutes"]),
                id=f"crawl_{priority}",
                name=f"Crawl {config['label']} Priority Sources",
                max_instances=1,
            )
            logger.info("  Registered job: %s (every %d min)", config["label"], config["interval_minutes"])

        # ── Editorial Calendar checker — every 30 min, re-evaluate event boosts
        self.scheduler.add_job(
            self._check_calendar_events,
            trigger=IntervalTrigger(minutes=30),
            id="calendar_check",
            name="Check Editorial Calendar Events",
            max_instances=1,
        )

        # ── Daily coverage report — at 23:00 UTC
        self.scheduler.add_job(
            self._daily_coverage_report,
            trigger="cron",
            hour=23,
            minute=0,
            id="daily_coverage",
            name="Daily Editorial Coverage Report",
            max_instances=1,
        )

        # ── Health check — every 6 hours
        self.scheduler.add_job(
            self._health_check,
            trigger="cron",
            hour="*/6",
            id="health_check",
            name="Source Health Check",
            max_instances=1,
        )

        self.scheduler.start()
        self._running = True
        logger.info("Scheduler started with %d jobs", len(self.scheduler.get_jobs()))

    def stop(self):
        if self.scheduler:
            self.scheduler.shutdown(wait=True)
            self._running = False
            logger.info("Scheduler stopped")

    def trigger_crawl(self, priority: Optional[str] = None):
        """Manually trigger a crawl for a specific priority level."""
        if priority:
            if priority in PRIORITY_SCHEDULE:
                job = self.scheduler.get_job(f"crawl_{priority}")
                if job:
                    job.modify(next_run_time=datetime.utcnow())
                    logger.info("Triggered manual crawl for %s priority", priority)
                    return True
            logger.warning("Unknown priority: %s", priority)
            return False
        return False

    def trigger_all(self):
        """Trigger all crawls immediately."""
        for priority in PRIORITY_SCHEDULE:
            self.trigger_crawl(priority)
        logger.info("Triggered manual crawl for all priority levels")
        return True

    def get_job_status(self):
        if not self.scheduler:
            return {"status": "stopped", "jobs": [], "priorities": PRIORITY_SCHEDULE}

        jobs = []
        for job in self.scheduler.get_jobs():
            jobs.append({
                "id": job.id,
                "name": job.name,
                "next_run_time": job.next_run_time.isoformat() if job.next_run_time else None,
                "trigger": str(job.trigger),
            })

        return {
            "status": "running" if self._running else "stopped",
            "jobs": jobs,
            "priority_schedule": PRIORITY_SCHEDULE,
        }

    def _crawl_by_priority(self, priority: str):
        """Crawl all sources matching this priority level."""
        logger.info("Starting scheduled crawl for %s priority sources...", priority)
        try:
            if not self.db:
                logger.warning("No database session available")
                return

            from app.services.crawl_service import CrawlService
            from app.models.source import Source
            from app.models.editorial import EditorialCalendar

            db = self.db()

            # ── Check for active calendar events that might boost sources
            now = datetime.utcnow()
            active_events = db.query(EditorialCalendar).filter(
                EditorialCalendar.is_active == 1,
                EditorialCalendar.start_date <= now,
                EditorialCalendar.end_date >= now,
            ).all()

            if active_events:
                logger.info("  Active calendar events: %d", len(active_events))
                for event in active_events:
                    logger.info("    - %s (boost: %s)", event.name, event.boost_priority)

            # ── Find sources whose effective priority matches
            sources = db.query(Source).filter(
                Source.is_active == 1,
                Source.status == "active",
            ).all()

            matched = []
            for src in sources:
                eff_priority = get_effective_priority(src, active_events)
                if eff_priority == priority:
                    matched.append(src)

            logger.info("  Found %d sources with %s priority", len(matched), priority)

            if not matched:
                db.close()
                return

            crawl_service = CrawlService(db)
            results = {"total": len(matched), "new_articles": 0, "crawled": 0, "errors": 0}

            for src in matched:
                try:
                    if not self._should_crawl(src, active_events):
                        continue
                    count = crawl_service.crawl_source(src.id)
                    results["new_articles"] += count
                    results["crawled"] += 1
                except Exception as e:
                    logger.error("  Crawl error for %s: %s", src.name, e)
                    results["errors"] += 1

            logger.info("  Crawl completed for %s: %s", priority, results)
            db.close()

        except Exception as e:
            logger.error("Error during %s priority crawl: %s", priority, e)

    def _should_crawl(self, source, calendar_events=None) -> bool:
        """Check if source should be crawled based on effective interval."""
        if not source.last_crawled_at:
            return True
        from datetime import timedelta
        interval = get_effective_interval(source, calendar_events)
        return datetime.utcnow() - source.last_crawled_at >= timedelta(minutes=interval)

    def _check_calendar_events(self):
        """Check for active or upcoming editorial calendar events."""
        logger.info("Checking editorial calendar events...")
        try:
            if not self.db:
                return
            from app.models.editorial import EditorialCalendar
            db = self.db()

            now = datetime.utcnow()
            active = db.query(EditorialCalendar).filter(
                EditorialCalendar.is_active == 1,
                EditorialCalendar.start_date <= now,
                EditorialCalendar.end_date >= now,
            ).all()

            if active:
                logger.info("Active calendar events: %d", len(active))
                for event in active:
                    logger.info("  - %s | boost: %s | topics: %s",
                                event.name, event.boost_priority, event.topics)

                    # If a critical event just started, trigger immediate crawl
                    if event.boost_priority == "critical":
                        self.trigger_crawl("critical")
                        logger.info("  Triggered immediate critical crawl due to event: %s", event.name)
            else:
                logger.info("No active calendar events")

            db.close()
        except Exception as e:
            logger.error("Error checking calendar events: %s", e)

    def _daily_coverage_report(self):
        """Generate daily editorial coverage report (Layer 8)."""
        logger.info("Generating daily editorial coverage report...")
        try:
            if not self.db:
                return
            from app.services.editorial_service import editorial_service
            db = self.db()
            report = editorial_service.generate_coverage_report(db)
            logger.info("Coverage report: %s", report.get("summary", "N/A"))
            db.close()
        except Exception as e:
            logger.error("Error generating coverage report: %s", e)

    def _health_check(self):
        """Check and report source health."""
        logger.info("Running source health check...")
        try:
            if not self.db:
                return
            from app.models.source import Source
            db = self.db()

            error_sources = db.query(Source).filter(
                Source.health == "error",
                Source.is_active == 1,
                Source.status == "active"
            ).all()

            if error_sources:
                logger.warning("Found %d sources with errors:", len(error_sources))
                for src in error_sources[:10]:
                    logger.warning("  - %s (errors: %d, priority: %s)", src.name, src.crawl_error_count or 0, src.priority)
            else:
                logger.info("All sources are healthy")

            # Also report priority distribution
            from sqlalchemy import func
            from collections import Counter
            all_active = db.query(Source).filter(Source.is_active == 1, Source.status == "active").all()
            priority_dist = Counter([s.priority or "normal" for s in all_active])
            logger.info("Priority distribution: %s", dict(priority_dist))

            db.close()
        except Exception as e:
            logger.error("Error during health check: %s", e)


# ── Singleton ──────────────────────────────────────────────────
scheduler_service = SchedulerService()