'''
models.py
Data models for the budget tracker: Transaction (a single income or
expense entry) plus re-exports of SavingsGoal and Budget so the rest
of the application can import everything from one place.
'''
import uuid
from datetime import date, datetime
from savingsgoal import SavingsGoal
from budget import Budget
__all__ = ["Transaction", "SavingsGoal", "Budget"]
class Transaction:
    """A single income or expense entry with date, category and amount."""
    KINDS = ("expense", "income")
    def __init__(self, kind, amount, category, description="", date_value=None, transaction_id=None):
        self.id = transaction_id or uuid.uuid4().hex[:10]
        kind = str(kind).strip().lower()
        if kind not in self.KINDS:
            raise ValueError("kind must be 'expense' or 'income'")
        self.kind = kind
        self.amount = self._validate_amount(amount)
        self.category = str(category).strip() or "Other"
        self.description = str(description)
        self.date = self._parse_date(date_value)
    @staticmethod
    def _validate_amount(amount):
        try:
            value = float(amount)
        except (TypeError, ValueError):
            raise ValueError("Amount must be a number")
        if value <= 0:
            raise ValueError("Amount must be greater than zero")
        return round(value, 2)
    @staticmethod
    def _parse_date(date_value):
        """Accept a date/datetime or 'YYYY-MM-DD' string; default to today."""
        if date_value in (None, ""):
            return date.today().isoformat()
        if isinstance(date_value, datetime):
            return date_value.date().isoformat()
        if isinstance(date_value, date):
            return date_value.isoformat()
        text = str(date_value).strip()
        try:
            return datetime.strptime(text, "%Y-%m-%d").date().isoformat()
        except ValueError:
            raise ValueError("Date must use the YYYY-MM-DD format")
    @property
    def month(self):
        """Month of the transaction as 'YYYY-MM'."""
        return self.date[:7]
    def to_dict(self):
        return {
            "id": self.id,
            "kind": self.kind,
            "amount": self.amount,
            "category": self.category,
            "description": self.description,
            "date": self.date,
        }
    @classmethod
    def from_dict(cls, data):
        data = data or {}
        return cls(
            kind=data.get("kind", "expense"),
            amount=data.get("amount", 0.0),
            category=data.get("category", "Other"),
            description=data.get("description", ""),
            date_value=data.get("date"),
            transaction_id=data.get("id"),
        )
    def __repr__(self):
        return f"Transaction({self.kind}, {self.amount:.2f}, {self.category}, {self.date})"