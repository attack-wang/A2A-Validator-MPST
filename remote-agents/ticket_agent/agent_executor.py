import logging

from agent import TicketAgent
from mpst_ext import MPSTValidatingExecutor


logger = logging.getLogger(__name__)


class TicketAgentExecutor(MPSTValidatingExecutor):
    """Ticket Agent executor with optional MPST runtime validation."""

    def __init__(self):
        super().__init__(delegate=None, role_name="Ticketagent")
        self.agent = TicketAgent()
        self._delegate = self
        logger.info(
            "TicketAgentExecutor initialized (validation=%s)",
            self.validation_enabled,
        )
