"""Seed AI news sources with full EOS metadata: Type, Priority, Topics."""
from app.core.database import SessionLocal
from app.models.source import Source
from app.models.category import Category
from app.models.topic import Topic
from app.models.editorial import EditorialCalendar
from app.core.editorial_policy import TOPIC_TAXONOMY
from slugify import slugify
from datetime import datetime


def seed_topics(db):
    """Seed topic taxonomy."""
    for topic in TOPIC_TAXONOMY:
        existing = db.query(Topic).filter(Topic.slug == topic["slug"]).first()
        if existing:
            existing.name = topic["name"]
            existing.priority_level = topic["priority"]
            existing.min_daily_articles = topic.get("min_daily", 0)
            existing.color = topic.get("color", "")
        else:
            db.add(Topic(
                name=topic["name"],
                slug=topic["slug"],
                priority_level=topic["priority"],
                min_daily_articles=topic.get("min_daily", 0),
                color=topic.get("color", ""),
                is_active=1,
            ))
    db.commit()
    print(f"[SEED] Topics: {len(TOPIC_TAXONOMY)} topics synced")


def seed_calendar_events(db):
    """Seed editorial calendar events for known AI conferences."""
    events = [
        {
            "name": "NeurIPS 2026",
            "slug": "neurips-2026",
            "description": "Annual Conference on Neural Information Processing Systems",
            "start_date": datetime(2026, 12, 2),
            "end_date": datetime(2026, 12, 8),
            "boost_priority": "critical",
            "boost_sources": "",
            "topics": "reasoning,benchmark,multimodal,robotics",
        },
        {
            "name": "ICML 2026",
            "slug": "icml-2026",
            "description": "International Conference on Machine Learning",
            "start_date": datetime(2026, 7, 12),
            "end_date": datetime(2026, 7, 18),
            "boost_priority": "critical",
            "boost_sources": "",
            "topics": "reasoning,benchmark,ai-infra",
        },
        {
            "name": "Google I/O 2026",
            "slug": "google-io-2026",
            "description": "Google's annual developer conference",
            "start_date": datetime(2026, 5, 14),
            "end_date": datetime(2026, 5, 15),
            "boost_priority": "critical",
            "boost_sources": "",
            "topics": "model-release,multimodal,api,agent",
        },
        {
            "name": "OpenAI DevDay 2026",
            "slug": "openai-devday-2026",
            "description": "OpenAI's annual developer conference",
            "start_date": datetime(2026, 11, 6),
            "end_date": datetime(2026, 11, 6),
            "boost_priority": "critical",
            "boost_sources": "",
            "topics": "model-release,agent,api,coding",
        },
    ]

    for event_data in events:
        existing = db.query(EditorialCalendar).filter(EditorialCalendar.slug == event_data["slug"]).first()
        if existing:
            for key, val in event_data.items():
                setattr(existing, key, val)
        else:
            db.add(EditorialCalendar(**event_data))
    db.commit()
    print(f"[SEED] Calendar events: {len(events)} events synced")


def seed_sources():
    db = SessionLocal()

    # ── Ensure category
    cat = db.query(Category).filter(Category.slug == "ai-news").first()
    if not cat:
        cat = Category(name="AI News", slug="ai-news", description="AI-related news and updates")
        db.add(cat)
        db.commit()

    # ── Seed topics
    seed_topics(db)

    # ── Seed calendar events
    seed_calendar_events(db)

    # ── Sources with full EOS metadata
    sources = [
        {
            "name": "OpenAI Blog",
            "url": "https://openai.com/blog",
            "feed_url": "https://openai.com/blog/rss.xml",
            "feed_type": "rss",
            "language": "en", "country": "us",
            "source_type": "official",      # Layer 3
            "priority": "critical",          # Layer 4
            "topics": "model-release,reasoning,agent,api,safety",  # Layer 2
            "editorial_tier": "s_tier",
            "editorial_role": "foundational / must-cover",
            "editorial_score": 95.0,
            "editorial_bucket": "essential",
            "credibility_score": 90.0,
            "crawl_interval_minutes": 5,
            "max_articles_per_fetch": 20,
        },
        {
            "name": "Google AI Blog",
            "url": "https://blog.google/technology/ai/",
            "feed_url": "https://blog.google/technology/ai/rss/",
            "feed_type": "rss",
            "language": "en", "country": "us",
            "source_type": "official",
            "priority": "critical",
            "topics": "model-release,multimodal,ai-infra,agent",
            "editorial_tier": "s_tier",
            "editorial_role": "foundational / must-cover",
            "editorial_score": 92.0,
            "editorial_bucket": "essential",
            "credibility_score": 88.0,
            "crawl_interval_minutes": 5,
            "max_articles_per_fetch": 20,
        },
        {
            "name": "DeepMind Blog",
            "url": "https://deepmind.google/discover/blog/",
            "feed_url": "https://deepmind.google/discover/blog/rss/",
            "feed_type": "rss",
            "language": "en", "country": "uk",
            "source_type": "official",
            "priority": "critical",
            "topics": "reasoning,robotics,multimodal,safety,benchmark",
            "editorial_tier": "s_tier",
            "editorial_role": "foundational / must-cover",
            "editorial_score": 93.0,
            "editorial_bucket": "essential",
            "credibility_score": 90.0,
            "crawl_interval_minutes": 5,
            "max_articles_per_fetch": 20,
        },
        {
            "name": "Anthropic News",
            "url": "https://www.anthropic.com/news",
            "feed_url": "",
            "feed_type": "web",
            "language": "en", "country": "us",
            "source_type": "official",
            "priority": "high",
            "topics": "model-release,reasoning,safety,agent,coding",
            "editorial_tier": "a_tier",
            "editorial_role": "primary reporting",
            "editorial_score": 85.0,
            "editorial_bucket": "authoritative",
            "credibility_score": 85.0,
            "crawl_interval_minutes": 15,
            "max_articles_per_fetch": 15,
        },
        {
            "name": "Meta AI Blog",
            "url": "https://ai.meta.com/blog/",
            "feed_url": "https://ai.meta.com/blog/rss/",
            "feed_type": "rss",
            "language": "en", "country": "us",
            "source_type": "official",
            "priority": "high",
            "topics": "open-source,multimodal,model-release,ai-infra",
            "editorial_tier": "a_tier",
            "editorial_role": "primary reporting",
            "editorial_score": 82.0,
            "editorial_bucket": "authoritative",
            "credibility_score": 82.0,
            "crawl_interval_minutes": 15,
            "max_articles_per_fetch": 20,
        },
        {
            "name": "Hugging Face Blog",
            "url": "https://huggingface.co/blog",
            "feed_url": "https://huggingface.co/blog/rss",
            "feed_type": "rss",
            "language": "en", "country": "us",
            "source_type": "developer",
            "priority": "high",
            "topics": "open-source,model-release,ai-infra,coding,agent",
            "editorial_tier": "a_tier",
            "editorial_role": "primary reporting",
            "editorial_score": 80.0,
            "editorial_bucket": "authoritative",
            "credibility_score": 80.0,
            "crawl_interval_minutes": 15,
            "max_articles_per_fetch": 20,
        },
        {
            "name": "arXiv AI Papers",
            "url": "https://arxiv.org/list/cs.AI/recent",
            "feed_url": "https://arxiv.org/rss/cs.AI",
            "feed_type": "rss",
            "language": "en", "country": "global",
            "source_type": "research",
            "priority": "normal",
            "topics": "reasoning,multimodal,benchmark,robotics,safety",
            "editorial_tier": "a_tier",
            "editorial_role": "primary reporting",
            "editorial_score": 88.0,
            "editorial_bucket": "authoritative",
            "credibility_score": 95.0,
            "crawl_interval_minutes": 30,
            "max_articles_per_fetch": 15,
        },
        {
            "name": "TechCrunch AI",
            "url": "https://techcrunch.com/category/artificial-intelligence/",
            "feed_url": "https://techcrunch.com/category/artificial-intelligence/feed/",
            "feed_type": "rss",
            "language": "en", "country": "us",
            "source_type": "media",
            "priority": "normal",
            "topics": "funding,model-release,policy,ai-infra",
            "editorial_tier": "b_tier",
            "editorial_role": "context & amplification",
            "editorial_score": 70.0,
            "editorial_bucket": "credible",
            "credibility_score": 75.0,
            "crawl_interval_minutes": 30,
            "max_articles_per_fetch": 15,
        },
        {
            "name": "AI Frontline",
            "url": "https://www.infoq.cn/topic/AI",
            "feed_url": "https://www.infoq.cn/feed/tag/AI",
            "feed_type": "rss",
            "language": "zh", "country": "cn",
            "source_type": "media",
            "priority": "normal",
            "topics": "model-release,agent,coding,ai-infra,policy",
            "editorial_tier": "b_tier",
            "editorial_role": "context & amplification",
            "editorial_score": 65.0,
            "editorial_bucket": "credible",
            "credibility_score": 70.0,
            "crawl_interval_minutes": 30,
            "max_articles_per_fetch": 15,
        },
        {
            "name": "Kimi Blog",
            "url": "https://www.kimi.com/blog/",
            "feed_url": "",
            "feed_type": "web",
            "language": "zh", "country": "cn",
            "source_type": "official",
            "priority": "normal",
            "topics": "model-release,reasoning,agent,coding",
            "editorial_tier": "b_tier",
            "editorial_role": "context & amplification",
            "editorial_score": 72.0,
            "editorial_bucket": "credible",
            "credibility_score": 75.0,
            "crawl_interval_minutes": 30,
            "max_articles_per_fetch": 10,
        },
        {
            "name": "Papers with Code",
            "url": "https://paperswithcode.com",
            "feed_url": "https://paperswithcode.com/rss/",
            "feed_type": "rss",
            "language": "en", "country": "global",
            "source_type": "research",
            "priority": "low",
            "topics": "benchmark,open-source,multimodal,reasoning",
            "editorial_tier": "c_tier",
            "editorial_role": "early-warning / niche",
            "editorial_score": 55.0,
            "editorial_bucket": "signal",
            "credibility_score": 85.0,
            "crawl_interval_minutes": 120,
            "max_articles_per_fetch": 20,
        },
        {
            "name": "The Batch by DeepLearning.AI",
            "url": "https://www.deeplearning.ai/the-batch/",
            "feed_url": "https://www.deeplearning.ai/the-batch/feed/",
            "feed_type": "rss",
            "language": "en", "country": "us",
            "source_type": "media",
            "priority": "low",
            "topics": "model-release,reasoning,agent,safety,policy,funding",
            "editorial_tier": "b_tier",
            "editorial_role": "context & amplification",
            "editorial_score": 75.0,
            "editorial_bucket": "credible",
            "credibility_score": 80.0,
            "crawl_interval_minutes": 120,
            "max_articles_per_fetch": 5,
        },
    ]

    added = 0
    skipped = 0
    updated = 0

    for data in sources:
        slug = slugify(data["name"])
        data["slug"] = slug
        data["is_active"] = 1
        data["status"] = "active"
        data["health"] = "healthy"

        exists = db.query(Source).filter(Source.slug == slug).first()

        if exists:
            needs_update = False
            for key, value in data.items():
                if getattr(exists, key, None) != value:
                    setattr(exists, key, value)
                    needs_update = True

            if needs_update:
                db.commit()
                updated += 1
                print(f"  Updated: {data['name']}")
            else:
                skipped += 1
                print(f"  Skipped: {data['name']}")
            continue

        source = Source(**data)
        db.add(source)
        added += 1
        print(f"  Added: {data['name']}")

    db.commit()
    print(f"\n[SEED] Sources: added={added}, updated={updated}, skipped={skipped}")


if __name__ == "__main__":
    seed_sources()