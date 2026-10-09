'''
models.py
Core data models for the Budget Tracker application.
Classes:
    Transaction -- a single income or expense record.
    SavingsGoal -- a savings goal with target amount and progress tracking.
'''
import uuid
from datetime import date
class Transaction:
    """A single financial transaction (income or expense)."""
    EXPENSE = "expense"
    INCOME = "income"
    def __init__(self, date_str, description, amount, category, t_type, tid=None):
        self.id = tid if tid is not None else str(uuid.uuid4())
        self.date = date_str
        self.description = description
        self.amount = round(float(amount), 2)
        self.category = category
        self.type = t_type
    def to_dict(self):
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
        return cls(
            data["date"],
            data["description"],
            data["amount"],
            data["category"],
            data["type"],
            tid=data.get("id"),
        )
    def is_expense(self):
        return self.type == self.EXPENSE
    def signed_amount(self):
        """Positive for income, negative for expenses."""
        return self.amount if self.type == self.INCOME else -self.amount
    def __repr__(self):
        return f"Transaction({self.date!r}, {self.description!r}, {self.amount}, {self.category!r}, {self.type!r})"
class SavingsGoal:
    """A savings goal with a target amount and accumulated contributions."""
    def __init__(self, name, target_amount, saved_amount=0.0, deadline=None, gid=None):
        self.id = gid if gid is not None else str(uuid.uuid4())
        self.name = name
        self.target_amount = round(float(target_amount), 2)
        self.saved_amount = round(float(saved_amount), 2)
        self.deadline = deadline  # ISO date string or None
    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "target_amount": self.target_amount,
            "saved_amount": self.saved_amount,
            "deadline": self.deadline,
        }
    @classmethod
    def from_dict(cls, data):
        return cls(
            data["name"],
            data["target_amount"],
            data.get("saved_amount", 0.0),
            data.get("deadline"),
            gid=data.get("id"),
        )
    def contribute(self, amount):
        self.saved_amount = round(self.saved_amount + float(amount), 2)
    def remaining(self):
        return max(0.0, round(self.target_amount - self.saved_amount, 2))
    def progress(self):
        """Return completion percentage (0-100), capped at 100."""
        if self.target_amount <= 0:
            return 100.0
        return min(100.0, (self.saved_amount / self.target_amount) * 100.0)
    def is_complete(self):
        return self.saved_amount >= self.target_amount
    def __repr__(self):
        return f"SavingsGoal({self.name!r}, target={self.target_amount}, saved={self.saved_amount})"