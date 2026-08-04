import logging

from agent import PublicTransportAgent
from mpst_ext import MPSTValidatingExecutor


logger = logging.getLogger(__name__)


class PublicTransportAgentExecutor(MPSTValidatingExecutor):
    """Public transport Agent executor with optional MPST validation."""

    def __init__(self):
        super().__init__(
            delegate=None,
            role_name="Publictransportagent",
        )
        self.agent = PublicTransportAgent()
        self._delegate = self
        logger.info(
            "PublicTransportAgentExecutor initialized (validation=%s)",
            self.validation_enabled,
        )
