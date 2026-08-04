import logging

from agent import TrainAgent
from mpst_ext import MPSTValidatingExecutor


logger = logging.getLogger(__name__)


class TrainAgentExecutor(MPSTValidatingExecutor):
    """Train Agent executor with optional MPST runtime validation."""

    def __init__(self):
        super().__init__(delegate=None, role_name="Trainagent")
        self.agent = TrainAgent()
        self._delegate = self
        logger.info(
            "TrainAgentExecutor initialized (validation=%s)",
            self.validation_enabled,
        )
