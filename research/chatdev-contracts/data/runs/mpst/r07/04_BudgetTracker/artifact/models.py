"""
models.py
Data models for the Budget Tracker application.
Defines the core data structures used throughout the application:
- Expense: a single expense record
- SavingsGoal: a savings target with progress tracking
Each model supports serialization to/from dictionaries so that data
can be persisted to JSON by the storage layer.
"""
from dataclasses import dataclass, field
from datetime import date, datetime
from typing import Optional
import uuid
@dataclass
class Expense:
    """Represents a single expense record."""
    amount: float
    category: str
    description: str = ""
    date_str: str = ""  # ISO format YYYY-MM-DD
    expense_id: str = field(default_factory=lambda: uuid.uuid4().hex[:12])
    def __post_init__(self):
        if not self.date_str:
            self.date_str = date.today().isoformat()
        self.amount = round(float(self.amount), 2)
    @property
    def date(self) -> date:
        """Return the expense date as a datetime.date object."""
        return datetime.strptime(self.date_str, "%Y-%m-%d").date()
    def to_dict(self) -> dict:
        """Serialize the expense to a dictionary for JSON storage."""
        return {
            "id": self.expense_id,
            "amount": self.amount,
            "category": self.category,
            "description": self.description,
            "date": self.date_str,
        }
    @classmethod
    def from_dict(cls, data: dict) -> "Expense":
        """Create an Expense from a dictionary (e.g., loaded from JSON)."""
        return cls(
            amount=float(data["amount"]),
            category=data["category"],
            description=data.get("description", ""),
            date_str=data.get("date", date.today().isoformat()),
            expense_id=data.get("id", uuid.uuid4().hex[:12]),
        )
@dataclass
class SavingsGoal:
    """Represents a savings goal with progress tracking."""
    name: str
    target_amount: float
    saved_amount: float = 0.0
    deadline_str: str = ""  # ISO format YYYY-MM-DD, optional
    goal_id: str = field(default_factory=lambda: uuid.uuid4().hex[:12])
    def __post_init__(self):
        self.target_amount = round(float(self.target_amount), 2)
        self.saved_amount = round(float(self.saved_amount), 2)
    @property
    def deadline(self) -> Optional[date]:
        """Return the goal deadline as a date, or None if not set."""
        if self.deadline_str:
            return datetime.strptime(self.deadline_str, "%Y-%m-%d").date()
        return None
    @property
    def progress(self) -> float:
        """Return progress toward the goal as a fraction in [0, 1]."""
        if self.target_amount <= 0:
            return 0.0
        return min(self.saved_amount / self.target_amount, 1.0)
    @property
    def remaining(self) -> float:
        """Return the amount still needed to reach the goal."""
        return max(self.target_amount - self.saved_amount, 0.0)
    @property
    def is_complete(self) -> bool:
        """Return True if the goal has been reached."""
        return self.saved_amount >= self.target_amount
    def contribute(self, amount: float) -> float:
        """Add money to the goal and return the new saved amount."""
        if amount <= 0:
            raise ValueError("Contribution must be positive.")
        self.saved_amount = round(self.saved_amount + float(amount), 2)
        return self.saved_amount
    def to_dict(self) -> dict:
        """Serialize the goal to a dictionary for JSON storage."""
        return {
            "id": self.goal_id,
            "name": self.name,
            "target_amount": self.target_amount,
            "saved_amount": self.saved_amount,
            "deadline": self.deadline_str,
        }
    @classmethod
    def from_dict(cls, data: dict) -> "SavingsGoal":
        """Create a SavingsGoal from a dictionary (e.g., loaded from JSON)."""
        return cls(
            name=data["name"],
            target_amount=float(data["target_amount"]),
            saved_amount=float(data.get("saved_amount", 0.0)),
            deadline_str=data.get("deadline", ""),
            goal_id=data.get("id", uuid.uuid4().hex[:12]),
        )