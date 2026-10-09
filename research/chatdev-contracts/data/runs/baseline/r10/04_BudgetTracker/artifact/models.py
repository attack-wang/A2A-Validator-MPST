'''
models.py
Data models for the Budget Tracker application.
This module defines the core domain objects:
  * Expense      - a single spending record (date, category, amount, description)
  * SavingsGoal  - a named savings target with the amount saved so far
Both classes know how to serialize themselves to/from plain dictionaries so
they can be persisted as JSON by the storage layer.
'''
import uuid
from datetime import datetime
class Expense:
    """A single expense record."""
    def __init__(self, amount, category, description="", date=None, expense_id=None):
        if amount is None or float(amount) < 0:
            raise ValueError("Expense amount must be a non-negative number.")
        self.id = expense_id if expense_id else str(uuid.uuid4())
        self.amount = round(float(amount), 2)
        self.category = category
        self.description = description
        self.date = date if date else datetime.now().strftime("%Y-%m-%d")
    @property
    def month(self):
        return self.date[:7]
    def to_dict(self):
        return {
            "id": self.id,
            "amount": self.amount,
            "category": self.category,
            "description": self.description,
            "date": self.date,
        }
    @classmethod
    def from_dict(cls, data):
        return cls(
            amount=data.get("amount", 0.0),
            category=data.get("category", "Other"),
            description=data.get("description", ""),
            date=data.get("date"),
            expense_id=data.get("id"),
        )
    def __repr__(self):
        return f"Expense({self.date}, {self.category}, {self.amount:.2f})"
class SavingsGoal:
    """A named savings target with progress tracking."""
    def __init__(self, name, target_amount, saved_amount=0.0, goal_id=None):
        if target_amount is None or float(target_amount) <= 0:
            raise ValueError("Savings target must be a positive number.")
        if saved_amount is None or float(saved_amount) < 0:
            raise ValueError("Saved amount must be a non-negative number.")
        self.id = goal_id if goal_id else str(uuid.uuid4())
        self.name = name
        self.target_amount = round(float(target_amount), 2)
        self.saved_amount = round(float(saved_amount), 2)
    @property
    def progress(self):
        if self.target_amount <= 0:
            return 0.0
        return min(self.saved_amount / self.target_amount * 100.0, 100.0)
    @property
    def remaining(self):
        return max(self.target_amount - self.saved_amount, 0.0)
    @property
    def is_complete(self):
        return self.saved_amount >= self.target_amount
    def deposit(self, amount):
        amount = float(amount)
        if amount <= 0:
            raise ValueError("Deposit must be a positive number.")
        self.saved_amount = round(self.saved_amount + amount, 2)
    def withdraw(self, amount):
        amount = float(amount)
        if amount <= 0:
            raise ValueError("Withdrawal must be a positive number.")
        if amount > self.saved_amount:
            raise ValueError(
                f"Cannot withdraw {amount:.2f}; only {self.saved_amount:.2f} saved."
            )
        self.saved_amount = round(self.saved_amount - amount, 2)
    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "target_amount": self.target_amount,
            "saved_amount": self.saved_amount,
        }
    @classmethod
    def from_dict(cls, data):
        return cls(
            name=data.get("name", "Goal"),
            target_amount=data.get("target_amount", 1.0),
            saved_amount=data.get("saved_amount", 0.0),
            goal_id=data.get("id"),
        )
    def __repr__(self):
        return f"SavingsGoal({self.name}, {self.saved_amount:.2f}/{self.target_amount:.2f})"