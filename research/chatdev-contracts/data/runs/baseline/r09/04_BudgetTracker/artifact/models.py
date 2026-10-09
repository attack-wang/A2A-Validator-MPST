'''
models.py
Data models for the ChatDev Budget Tracker application.
Defines the Transaction and SavingsGoal classes together with the
shared DATE_FORMAT constant and the EXPENSE_CATEGORIES /
INCOME_CATEGORIES lists used across storage, analytics and gui.
'''
import uuid
from datetime import datetime
DATE_FORMAT = "%Y-%m-%d"
EXPENSE_CATEGORIES = [
    "Food & Dining",
    "Groceries",
    "Housing",
    "Transportation",
    "Utilities",
    "Entertainment",
    "Healthcare",
    "Shopping",
    "Education",
    "Travel",
    "Other",
]
INCOME_CATEGORIES = [
    "Salary",
    "Freelance",
    "Investment",
    "Refund",
    "Gift",
    "Other",
]
class Transaction:
    """A single income or expense record with validation and JSON support."""
    def __init__(self, date, description, amount, category,
                 transaction_type, transaction_id=None):
        if transaction_type not in ("expense", "income"):
            raise ValueError("transaction_type must be 'expense' or 'income'")
        try:
            amount = round(float(amount), 2)
        except (TypeError, ValueError):
            raise ValueError("amount must be a number")
        if amount <= 0:
            raise ValueError("amount must be positive")
        try:
            datetime.strptime(str(date), DATE_FORMAT)
        except (TypeError, ValueError):
            raise ValueError("date must be in YYYY-MM-DD format")
        if not str(description).strip():
            raise ValueError("description must not be empty")
        if not str(category).strip():
            raise ValueError("category must not be empty")
        self.id = transaction_id or uuid.uuid4().hex[:12]
        self.date = str(date)
        self.description = str(description)
        self.amount = amount
        self.category = str(category)
        self.type = transaction_type
    def to_dict(self):
        """Serialize the transaction into a JSON-compatible dictionary."""
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
        """Rebuild a Transaction instance from its dictionary form."""
        return cls(
            date=data["date"],
            description=data["description"],
            amount=data["amount"],
            category=data["category"],
            transaction_type=data["type"],
            transaction_id=data.get("id"),
        )
class SavingsGoal:
    """A savings goal with a target amount, saved amount and progress helpers."""
    def __init__(self, name, target_amount, saved_amount=0.0, goal_id=None):
        try:
            target_amount = round(float(target_amount), 2)
            saved_amount = round(float(saved_amount), 2)
        except (TypeError, ValueError):
            raise ValueError("amounts must be numbers")
        if target_amount <= 0:
            raise ValueError("target_amount must be positive")
        if saved_amount < 0:
            raise ValueError("saved_amount cannot be negative")
        if not str(name).strip():
            raise ValueError("name must not be empty")
        self.id = goal_id or uuid.uuid4().hex[:12]
        self.name = str(name)
        self.target_amount = target_amount
        self.saved_amount = saved_amount
    @property
    def remaining(self):
        """Amount still required to reach the target (never negative)."""
        return round(max(0.0, self.target_amount - self.saved_amount), 2)
    @property
    def progress(self):
        """Completion percentage, capped at 100%."""
        return round(min(100.0, self.saved_amount / self.target_amount * 100.0), 1)
    def deposit(self, amount):
        """Add a positive amount to the saved total."""
        try:
            amount = round(float(amount), 2)
        except (TypeError, ValueError):
            raise ValueError("amount must be a number")
        if amount <= 0:
            raise ValueError("amount must be positive")
        self.saved_amount = round(self.saved_amount + amount, 2)
    def withdraw(self, amount):
        """Remove a positive amount from the saved total (floored at zero)."""
        try:
            amount = round(float(amount), 2)
        except (TypeError, ValueError):
            raise ValueError("amount must be a number")
        if amount <= 0:
            raise ValueError("amount must be positive")
        self.saved_amount = round(max(0.0, self.saved_amount - amount), 2)
    def to_dict(self):
        """Serialize the goal into a JSON-compatible dictionary."""
        return {
            "id": self.id,
            "name": self.name,
            "target_amount": self.target_amount,
            "saved_amount": self.saved_amount,
        }
    @classmethod
    def from_dict(cls, data):
        """Rebuild a SavingsGoal instance from its dictionary form."""
        return cls(
            name=data["name"],
            target_amount=data["target_amount"],
            saved_amount=data.get("saved_amount", 0.0),
            goal_id=data.get("id"),
        )