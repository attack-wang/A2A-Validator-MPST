import logging

from agent import FlightAgent
from mpst_ext import MPSTValidatingExecutor


logger = logging.getLogger(__name__)


class FlightAgentExecutor(MPSTValidatingExecutor):
    """Flight Agent executor with optional MPST runtime validation."""

    def __init__(self):
        super().__init__(delegate=None, role_name="Flightagent")
        self.agent = FlightAgent()
        self._delegate = self
        logger.info(
            "FlightAgentExecutor initialized (validation=%s)",
            self.validation_enabled,
        )
