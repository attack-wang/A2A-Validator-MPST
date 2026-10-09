'''
models.py
Defines the core data models for the Budget Tracker application:
Transaction, SavingsGoal, and Budget. Each model provides serialization
(to_dict / from_dict) helpers so the storage layer can persist them as JSON.
'''
import uuid
from datetime import datetime
class Transaction:
    """A single financial transaction, either an expense or an income."""
    EXPENSE = "expense"
    INCOME = "income"
    def __init__(self, amount, category, description="", date=None,
                 transaction_type=EXPENSE, transaction_id=None):
        self.id = transaction_id if transaction_id else str(uuid.uuid4())
        self.amount = round(float(amount), 2)
        self.category = category
        self.description = description
        self.date = date if date else datetime.now().strftime("%Y-%m-%d")
        self.type = transaction_type
    def to_dict(self):
        """Serialize the transaction to a dictionary for JSON storage."""
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
        """Rebuild a Transaction instance from a dictionary."""
        return cls(
            amount=data["amount"],
            category=data["category"],
            description=data.get("description", ""),
            date=data.get("date"),
            transaction_type=data.get("type", cls.EXPENSE),
            transaction_id=data.get("id"),
        )
    def __str__(self):
        sign = "-" if self.type == self.EXPENSE else "+"
        return (f"[{self.id[:8]}] {self.date} | {self.type.capitalize():7s} | "
                f"{sign}${self.amount:>10.2f} | {self.category:<15} | {self.description}")
class SavingsGoal:
    """A savings goal with a target amount and optional deadline."""
    def __init__(self, name, target_amount, current_amount=0.0, deadline=None, goal_id=None):
        self.id = goal_id if goal_id else str(uuid.uuid4())
        self.name = name
        self.target_amount = round(float(target_amount), 2)
        self.current_amount = round(float(current_amount), 2)
        self.deadline = deadline  # "YYYY-MM-DD" or None
    @property
    def progress_percent(self):
        """Percentage of the goal completed (0-100)."""
        if self.target_amount <= 0:
            return 100.0
        return min(100.0, (self.current_amount / self.target_amount) * 100)
    @property
    def remaining(self):
        """Amount still needed to reach the target."""
        return max(0.0, self.target_amount - self.current_amount)
    def contribute(self, amount):
        """Add money to the goal; returns the new current amount."""
        if amount <= 0:
            raise ValueError("Contribution must be positive.")
        self.current_amount = round(self.current_amount + float(amount), 2)
        return self.current_amount
    def withdraw(self, amount):
        """Remove money from the goal (e.g., correction); returns new current amount."""
        if amount <= 0:
            raise ValueError("Withdrawal must be positive.")
        self.current_amount = round(max(0.0, self.current_amount - float(amount)), 2)
        return self.current_amount
    def to_dict(self):
        """Serialize the savings goal to a dictionary for JSON storage."""
        return {
            "id": self.id,
            "name": self.name,
            "target_amount": self.target_amount,
            "current_amount": self.current_amount,
            "deadline": self.deadline,
        }
    @classmethod
    def from_dict(cls, data):
        """Rebuild a SavingsGoal instance from a dictionary."""
        return cls(
            name=data["name"],
            target_amount=data["target_amount"],
            current_amount=data.get("current_amount", 0.0),
            deadline=data.get("deadline"),
            goal_id=data.get("id"),
        )
    def __str__(self):
        deadline = f", deadline {self.deadline}" if self.deadline else ""
        return (f"[{self.id[:8]}] {self.name}: ${self.current_amount:,.2f} of "
                f"${self.target_amount:,.2f} ({self.progress_percent:.1f}%){deadline}")
class Budget:
    """A monthly spending limit for a specific expense category."""
    def __init__(self, category, monthly_limit, budget_id=None):
        self.id = budget_id if budget_id else str(uuid.uuid4())
        self.category = category
        self.monthly_limit = round(float(monthly_limit), 2)
    def to_dict(self):
        """Serialize the budget to a dictionary for JSON storage."""
        return {
            "id": self.id,
            "category": self.category,
            "monthly_limit": self.monthly_limit,
        }
    @classmethod
    def from_dict(cls, data):
        """Rebuild a Budget instance from a dictionary."""
        return cls(
            category=data["category"],
            monthly_limit=data["monthly_limit"],
            budget_id=data.get("id"),
        )
    def __str__(self):
        return f"[{self.id[:8]}] {self.category}: ${self.monthly_limit:,.2f} / month"