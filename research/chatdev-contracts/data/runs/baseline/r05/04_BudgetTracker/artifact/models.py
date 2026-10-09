'''
models.py
Data models for the Budget Tracker application.
Defines:
- Transaction: a single income or expense record.
- Budget: a monthly spending limit for a category.
- SavingsGoal: a target amount the user wants to save toward.
Also defines default categories and transaction type constants.
'''
import uuid
from datetime import datetime
# Constants ---------------------------------------------------------------
TRANSACTION_TYPES = ("expense", "income")
DEFAULT_CATEGORIES = (
    "Food",
    "Housing",
    "Transportation",
    "Utilities",
    "Entertainment",
    "Healthcare",
    "Shopping",
    "Education",
    "Other",
)
DATE_FORMAT = "%Y-%m-%d"
class Transaction:
    """A single financial transaction (expense or income)."""
    def __init__(self, date, description, amount, category, t_type,
                 transaction_id=None):
        self.id = transaction_id or str(uuid.uuid4())
        self.date = date
        self.description = description
        self.amount = round(float(amount), 2)
        self.category = category
        self.type = t_type
    # -- validation helpers ------------------------------------------------
    @staticmethod
    def is_valid_date(date_str):
        """Return True if date_str matches YYYY-MM-DD."""
        try:
            datetime.strptime(date_str, DATE_FORMAT)
            return True
        except (TypeError, ValueError):
            return False
    @staticmethod
    def is_valid_amount(amount):
        """Return True if amount is a positive number."""
        try:
            return float(amount) > 0
        except (TypeError, ValueError):
            return False
    # -- derived info -------------------------------------------------------
    @property
    def month(self):
        """Return the month key ('YYYY-MM') for this transaction."""
        return self.date[:7]
    # -- serialization ------------------------------------------------------
    def to_dict(self):
        """Convert the transaction to a plain dictionary for storage."""
        return {
            "id": self.id,
            "date": self.date,
            "description": self.description,
            "amount": self.amount,
            "category": self.category,
            "type": self.type,
        }
    @classmethod
    def from_dict(cls, data):
        """Rebuild a Transaction from its dictionary representation."""
        return cls(
            date=data["date"],
            description=data["description"],
            amount=data["amount"],
            category=data["category"],
            t_type=data["type"],
            transaction_id=data.get("id"),
        )
class Budget:
    """A monthly spending limit for one expense category."""
    def __init__(self, category, monthly_limit):
        self.category = category
        self.monthly_limit = round(float(monthly_limit), 2)
    def to_dict(self):
        """Convert the budget to a plain dictionary for storage."""
        return {"category": self.category, "monthly_limit": self.monthly_limit}
    @classmethod
    def from_dict(cls, data):
        """Rebuild a Budget from its dictionary representation."""
        return cls(category=data["category"],
                   monthly_limit=data["monthly_limit"])
class SavingsGoal:
    """A savings goal with a target amount and running progress."""
    def __init__(self, name, target_amount, deadline=None, saved_amount=0.0,
                 goal_id=None):
        self.id = goal_id or str(uuid.uuid4())
        self.name = name
        self.target_amount = round(float(target_amount), 2)
        self.deadline = deadline  # 'YYYY-MM-DD' or None
        self.saved_amount = round(float(saved_amount), 2)
    # -- progress helpers ---------------------------------------------------
    def contribute(self, amount):
        """Add money to the goal's saved amount."""
        self.saved_amount = round(self.saved_amount + float(amount), 2)
    def progress_percent(self):
        """Return progress toward the target as a percentage (0-100+)."""
        if self.target_amount <= 0:
            return 0.0
        return min(100.0, (self.saved_amount / self.target_amount) * 100.0)
    def remaining_amount(self):
        """Return how much more is needed to reach the target."""
        return max(0.0, round(self.target_amount - self.saved_amount, 2))
    def is_complete(self):
        """Return True when the goal has been fully funded."""
        return self.saved_amount >= self.target_amount
    # -- serialization ------------------------------------------------------
    def to_dict(self):
        """Convert the goal to a plain dictionary for storage."""
        return {
            "id": self.id,
            "name": self.name,
            "target_amount": self.target_amount,
            "deadline": self.deadline,
            "saved_amount": self.saved_amount,
        }
    @classmethod
    def from_dict(cls, data):
        """Rebuild a SavingsGoal from its dictionary representation."""
        return cls(
            name=data["name"],
            target_amount=data["target_amount"],
            deadline=data.get("deadline"),
            saved_amount=data.get("saved_amount", 0.0),
            goal_id=data.get("id"),
        )