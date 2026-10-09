'''
models.py
Data models for the Budget Tracker application.
Defines the core domain objects:
    * Transaction    -- a single income, expense, or savings entry.
    * SavingsGoal    -- a named target amount the user wants to reach.
    * CategoryBudget -- a monthly spending limit for one category.
Each model validates its own fields on creation and knows how to
serialize itself to/from plain dictionaries so the storage layer
(storage.py) can persist them as JSON.
'''
from dataclasses import dataclass, field
from datetime import date
from typing import Optional
import uuid
TRANSACTION_TYPES = ("income", "expense", "savings")
def _generate_id() -> str:
    """Return a short, unique identifier string."""
    return uuid.uuid4().hex[:12]
def _today_iso() -> str:
    """Return today's date as an ISO-8601 string (YYYY-MM-DD)."""
    return date.today().isoformat()
def is_valid_date(value) -> bool:
    """Return True if *value* is a valid ISO-8601 date string."""
    try:
        date.fromisoformat(str(value))
        return True
    except (TypeError, ValueError):
        return False
@dataclass
class Transaction:
    """A single tracked money event (income, expense, or savings deposit)."""
    amount: float
    category: str
    t_type: str
    description: str = ""
    date: str = field(default_factory=_today_iso)
    id: str = field(default_factory=_generate_id)
    def __post_init__(self):
        try:
            self.amount = round(float(self.amount), 2)
        except (TypeError, ValueError):
            raise ValueError(f"Amount must be a number, got {self.amount!r}")
        if self.amount <= 0:
            raise ValueError("Amount must be greater than zero.")
        if self.t_type not in TRANSACTION_TYPES:
            raise ValueError(
                f"Transaction type must be one of {TRANSACTION_TYPES}, got {self.t_type!r}"
            )
        self.category = str(self.category).strip()
        if not self.category:
            raise ValueError("Category cannot be empty.")
        if not is_valid_date(self.date):
            raise ValueError(f"Date must be YYYY-MM-DD, got {self.date!r}")
        self.description = str(self.description).strip()
    def to_dict(self) -> dict:
        """Return a plain-dictionary representation for JSON persistence."""
        return {
            "id": self.id,
            "amount": self.amount,
            "category": self.category,
            "type": self.t_type,
            "description": self.description,
            "date": self.date,
        }
    @classmethod
    def from_dict(cls, data: dict) -> "Transaction":
        """Rebuild a Transaction from its dictionary representation."""
        return cls(
            amount=data["amount"],
            category=data["category"],
            t_type=data["type"],
            description=data.get("description", ""),
            date=data.get("date", _today_iso()),
            id=data.get("id", _generate_id()),
        )
@dataclass
class SavingsGoal:
    """A named savings target, e.g. 'Emergency Fund' with a $5,000 target."""
    name: str
    target_amount: float
    deadline: Optional[str] = None
    id: str = field(default_factory=_generate_id)
    def __post_init__(self):
        self.name = str(self.name).strip()
        if not self.name:
            raise ValueError("Goal name cannot be empty.")
        try:
            self.target_amount = round(float(self.target_amount), 2)
        except (TypeError, ValueError):
            raise ValueError(f"Target amount must be a number, got {self.target_amount!r}")
        if self.target_amount <= 0:
            raise ValueError("Target amount must be greater than zero.")
        if self.deadline in ("", None):
            self.deadline = None
        elif not is_valid_date(self.deadline):
            raise ValueError(f"Deadline must be YYYY-MM-DD, got {self.deadline!r}")
    def to_dict(self) -> dict:
        """Return a plain-dictionary representation for JSON persistence."""
        return {
            "id": self.id,
            "name": self.name,
            "target_amount": self.target_amount,
            "deadline": self.deadline,
        }
    @classmethod
    def from_dict(cls, data: dict) -> "SavingsGoal":
        """Rebuild a SavingsGoal from its dictionary representation."""
        return cls(
            name=data["name"],
            target_amount=data["target_amount"],
            deadline=data.get("deadline"),
            id=data.get("id", _generate_id()),
        )
@dataclass
class CategoryBudget:
    """A monthly spending limit for one expense category."""
    name: str
    monthly_limit: float
    def __post_init__(self):
        self.name = str(self.name).strip()
        if not self.name:
            raise ValueError("Budget category cannot be empty.")
        try:
            self.monthly_limit = round(float(self.monthly_limit), 2)
        except (TypeError, ValueError):
            raise ValueError(f"Monthly limit must be a number, got {self.monthly_limit!r}")
        if self.monthly_limit <= 0:
            raise ValueError("Monthly limit must be greater than zero.")
    def to_dict(self) -> dict:
        """Return a plain-dictionary representation for JSON persistence."""
        return {"name": self.name, "monthly_limit": self.monthly_limit}
    @classmethod
    def from_dict(cls, data: dict) -> "CategoryBudget":
        """Rebuild a CategoryBudget from its dictionary representation."""
        return cls(name=data["name"], monthly_limit=data["monthly_limit"])