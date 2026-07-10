"""Scheduler - stub."""
import logging
logger = logging.getLogger(__name__)


class SchedulerService:
    def __init__(self, db=None):
        self.db = db

    def start(self):
        logger.info("Scheduler stub started (no-op)")

    def stop(self):
        pass
