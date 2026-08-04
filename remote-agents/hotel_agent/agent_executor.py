import logging

from agent import HotelAgent
from mpst_ext import MPSTValidatingExecutor


logger = logging.getLogger(__name__)


class HotelAgentExecutor(MPSTValidatingExecutor):
    """Hotel Agent executor with optional MPST runtime validation."""

    def __init__(self):
        super().__init__(delegate=None, role_name="Hotelagent")
        self.agent = HotelAgent()
        self._delegate = self
        logger.info(
            "HotelAgentExecutor initialized (validation=%s)",
            self.validation_enabled,
        )
