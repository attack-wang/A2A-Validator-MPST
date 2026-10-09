'''
models.py
Data models for the Budget Tracker application.
Defines lightweight dataclass objects that represent the core domain
entities of the application:
- Transaction: a single income or expense record.
- SavingsGoal: a named savings target with a monetary goal amount.
These models are intentionally free of any GUI or database code so they
can be shared between the persistence layer (database.py) and the
presentation layer (gui.py / dialogs.py).
'''
from dataclasses import dataclass
from typing import Optional
TRANSACTION_EXPENSE = "expense"
TRANSACTION_INCOME = "income"
@dataclass
class Transaction:
    """A single financial transaction (either an expense or income)."""
    id: Optional[int]
    date: str          # ISO date string, format: YYYY-MM-DD
    description: str
    amount: float      # always positive; direction given by `type`
    category: str
    type: str          # TRANSACTION_EXPENSE or TRANSACTION_INCOME
    @property
    def signed_amount(self) -> float:
        """Amount as a signed value: negative for expenses, positive for income."""
        return self.amount if self.type == TRANSACTION_INCOME else -self.amount
@dataclass
class SavingsGoal:
    """A named savings target the user wants to reach."""
    id: Optional[int]
    name: str
    target_amount: float
    created_date: str  # ISO date string, format: YYYY-MM-DD
    def progress(self, current_savings: float) -> float:
        """Return goal completion as a fraction in [0, 1]."""
        if self.target_amount <= 0:
            return 0.0
        return max(0.0, min(1.0, current_savings / self.target_amount))