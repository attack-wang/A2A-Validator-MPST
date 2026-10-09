'''
models.py
Data models for the Budget Tracker application.
Defines the core entities used throughout the application:
transactions (expenses and income), budgets, and savings goals.
Each model provides serialization helpers so the storage layer
can persist them as JSON.
'''
import uuid
from datetime import datetime
class Transaction:
    """Represents a single financial transaction (expense or income)."""
    def __init__(self, amount, category, description="", date=None,
                 transaction_type="expense", transaction_id=None):
        self.id = transaction_id if transaction_id else str(uuid.uuid4())
        self.amount = float(amount)
        self.category = category
        self.description = description
        self.date = date if date else datetime.now().strftime("%Y-%m-%d")
        self.type = transaction_type
    def to_dict(self):
        return {
            "id": self.id,
            "amount": self.amount,
            "category": self.category,
            "description": self.description,
            "date": self.date,
            "type": self.type,
        }
    @classmethod
    def from_dict(cls, data):
        return cls(
            amount=data["amount"],
            category=data["category"],
            description=data.get("description", ""),
            date=data.get("date"),
            transaction_type=data.get("type", "expense"),
            transaction_id=data.get("id"),
        )
class Budget:
    """Represents a monthly spending limit for a category."""
    def __init__(self, category, monthly_limit, budget_id=None):
        self.id = budget_id if budget_id else str(uuid.uuid4())
        self.category = category
        self.monthly_limit = float(monthly_limit)
    def to_dict(self):
        return {
            "id": self.id,
            "category": self.category,
            "monthly_limit": self.monthly_limit,
        }
    @classmethod
    def from_dict(cls, data):
        return cls(
            category=data["category"],
            monthly_limit=data["monthly_limit"],
            budget_id=data.get("id"),
        )
class SavingsGoal:
    """Represents a savings goal with a target amount and optional deadline."""
    def __init__(self, name, target_amount, deadline=None,
                 saved_amount=0.0, goal_id=None):
        self.id = goal_id if goal_id else str(uuid.uuid4())
        self.name = name
        self.target_amount = float(target_amount)
        self.deadline = deadline  # "YYYY-MM-DD" or None
        self.saved_amount = float(saved_amount)
    @property
    def progress(self):
        """Return progress toward the goal as a percentage (0-100)."""
        if self.target_amount <= 0:
            return 0.0
        return min(100.0, (self.saved_amount / self.target_amount) * 100.0)
    @property
    def remaining(self):
        """Return the amount still needed to reach the goal."""
        return max(0.0, self.target_amount - self.saved_amount)
    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "target_amount": self.target_amount,
            "deadline": self.deadline,
            "saved_amount": self.saved_amount,
        }
    @classmethod
    def from_dict(cls, data):
        return cls(
            name=data["name"],
            target_amount=data["target_amount"],
            deadline=data.get("deadline"),
            saved_amount=data.get("saved_amount", 0.0),
            goal_id=data.get("id"),
        )