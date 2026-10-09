'''
models.py
Data models for the budget tracker application.
This module defines the core data structures used throughout the
application: Expense records and SavingsGoal objects. Each model
provides serialization helpers (to_dict / from_dict) so that the
storage layer can persist them as JSON.
'''
import uuid
from datetime import datetime
class Expense:
    """Represents a single expense record."""
    def __init__(self, amount, category, description="", date=None, expense_id=None):
        self.id = expense_id if expense_id else str(uuid.uuid4())
        self.amount = float(amount)
        self.category = category
        self.description = description
        self.date = date if date else datetime.now().strftime("%Y-%m-%d")
    def to_dict(self):
        """Convert the expense to a dictionary for JSON serialization."""
        return {
            "id": self.id,
            "amount": self.amount,
            "category": self.category,
            "description": self.description,
            "date": self.date,
        }
    @classmethod
    def from_dict(cls, data):
        """Create an Expense instance from a dictionary."""
        return cls(
            amount=data["amount"],
            category=data["category"],
            description=data.get("description", ""),
            date=data.get("date"),
            expense_id=data.get("id"),
        )
class SavingsGoal:
    """Represents a savings goal with a target amount and current progress."""
    def __init__(self, name, target_amount, current_amount=0.0, goal_id=None):
        self.id = goal_id if goal_id else str(uuid.uuid4())
        self.name = name
        self.target_amount = float(target_amount)
        self.current_amount = float(current_amount)
    @property
    def progress_percent(self):
        """Percentage of the goal that has been reached (0-100)."""
        if self.target_amount <= 0:
            return 0.0
        return min(100.0, (self.current_amount / self.target_amount) * 100.0)
    @property
    def is_complete(self):
        """True when the current amount meets or exceeds the target."""
        return self.current_amount >= self.target_amount
    def to_dict(self):
        """Convert the savings goal to a dictionary for JSON serialization."""
        return {
            "id": self.id,
            "name": self.name,
            "target_amount": self.target_amount,
            "current_amount": self.current_amount,
        }
    @classmethod
    def from_dict(cls, data):
        """Create a SavingsGoal instance from a dictionary."""
        return cls(
            name=data["name"],
            target_amount=data["target_amount"],
            current_amount=data.get("current_amount", 0.0),
            goal_id=data.get("id"),
        )