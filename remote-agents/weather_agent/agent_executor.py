import logging

from agent import WeatherAgent
from mpst_ext import MPSTValidatingExecutor


logger = logging.getLogger(__name__)


class WeatherAgentExecutor(MPSTValidatingExecutor):
    """Weather Agent executor with optional MPST runtime validation."""

    def __init__(self):
        super().__init__(delegate=None, role_name="Weatheragent")
        self.agent = WeatherAgent()
        self._delegate = self
        logger.info(
            "WeatherAgentExecutor initialized (validation=%s)",
            self.validation_enabled,
        )
