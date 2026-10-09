'''Data models for the budget tracker application.'''
from dataclasses import dataclass
@dataclass
class Transaction:
    """Represents a single income or expense entry."""
    id: int
    date: str          # ISO format: YYYY-MM-DD
    tx_type: str       # 'expense' or 'income'
    category: str
    amount: float
    description: str
@dataclass
class Budget:
    """Represents a monthly spending limit for a category."""
    category: str
    monthly_limit: float
@dataclass
class SavingsGoal:
    """Represents a savings goal with progress tracking."""
    id: int
    name: str
    target_amount: float
    saved_amount: float
    deadline: str      # ISO format: YYYY-MM-DD (may be empty)
    @property
    def progress(self) -> float:
        """Return completion percentage (0-100)."""
        if self.target_amount <= 0:
            return 0.0
        return min(100.0, (self.saved_amount / self.target_amount) * 100.0)
    @property
    def remaining(self) -> float:
        """Return the amount still needed to reach the goal."""
        return max(0.0, self.target_amount - self.saved_amount)