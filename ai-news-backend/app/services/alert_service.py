"""Alert Service - stub."""
import logging
logger = logging.getLogger(__name__)


class AlertService:
    def __init__(self, db=None):
        self.db = db

    def check_alerts(self):
        pass
