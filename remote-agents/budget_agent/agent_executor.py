import logging

from agent import BudgetAgent
from mpst_ext import MPSTValidatingExecutor


logger = logging.getLogger(__name__)


class BudgetAgentExecutor(MPSTValidatingExecutor):
    """Budget Agent executor with optional MPST runtime validation."""

    def __init__(self):
        super().__init__(delegate=None, role_name="Budgetagent")
        self.agent = BudgetAgent()
        self._delegate = self
        logger.info(
            "BudgetAgentExecutor initialized (validation=%s)",
            self.validation_enabled,
        )
