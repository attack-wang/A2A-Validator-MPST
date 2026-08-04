import logging

from agent import TransportSelectAgent
from mpst_ext import MPSTValidatingExecutor


logger = logging.getLogger(__name__)


class TransportSelectAgentExecutor(MPSTValidatingExecutor):
    """Transport-selection executor with optional MPST validation."""

    def __init__(self):
        super().__init__(
            delegate=None,
            role_name="Transportselectagent",
        )
        self.agent = TransportSelectAgent()
        self._delegate = self
        logger.info(
            "TransportSelectAgentExecutor initialized (validation=%s)",
            self.validation_enabled,
        )
