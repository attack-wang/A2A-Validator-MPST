import logging

from agent import GuideAgent
from mpst_ext import MPSTValidatingExecutor


logger = logging.getLogger(__name__)


class GuideAgentExecutor(MPSTValidatingExecutor):
    """Guide Agent executor with optional MPST runtime validation."""

    def __init__(self):
        super().__init__(delegate=None, role_name="Guideagent")
        self.agent = GuideAgent()
        self._delegate = self
        logger.info(
            "GuideAgentExecutor initialized (validation=%s)",
            self.validation_enabled,
        )
