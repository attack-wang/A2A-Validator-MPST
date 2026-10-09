'''
models.py
Defines the core data models for the Budget Tracker application.
Classes:
    Transaction: Represents a single income or expense record with
        validation, serialization, and deserialization support.
    Category: Provides the predefined expense and income categories
        used throughout the application.
'''
import uuid
from datetime import datetime
class Transaction:
    """Represents a single financial transaction (income or expense)."""
    EXPENSE = "expense"
    INCOME = "income"
    VALID_TYPES = (EXPENSE, INCOME)
    DATE_FORMAT = "%Y-%m-%d"
    def __init__(self, date, description, amount, category, ttype, transaction_id=None):
        """
        Initialize a Transaction.
        Args:
            date (str): Transaction date in 'YYYY-MM-DD' format.
            description (str): Short human-readable description.
            amount (float): Positive monetary value.
            category (str): Category name.
            ttype (str): Either 'expense' or 'income'.
            transaction_id (str, optional): Unique id; generated when omitted.
        Raises:
            ValueError: If any argument fails validation.
        """
        self.id = transaction_id if transaction_id else str(uuid.uuid4())
        self.date = self._validate_date(date)
        self.description = self._validate_description(description)
        self.amount = self._validate_amount(amount)
        self.category = self._validate_category(category)
        self.type = self._validate_type(ttype)
    # --- validation helpers -------------------------------------------------
    @staticmethod
    def _validate_date(date):
        try:
            datetime.strptime(str(date).strip(), Transaction.DATE_FORMAT)
        except (ValueError, TypeError):
            raise ValueError("Date must be in YYYY-MM-DD format.")
        return str(date).strip()
    @staticmethod
    def _validate_description(description):
        text = str(description).strip()
        if not text:
            raise ValueError("Description cannot be empty.")
        return text
    @staticmethod
    def _validate_amount(amount):
        try:
            value = float(amount)
        except (ValueError, TypeError):
            raise ValueError("Amount must be a number.")
        if value <= 0:
            raise ValueError("Amount must be greater than zero.")
        return round(value, 2)
    @staticmethod
    def _validate_category(category):
        text = str(category).strip()
        if not text:
            raise ValueError("Category cannot be empty.")
        return text
    @staticmethod
    def _validate_type(ttype):
        text = str(ttype).strip().lower()
        if text not in Transaction.VALID_TYPES:
            raise ValueError("Type must be 'expense' or 'income'.")
        return text
    # --- serialization ------------------------------------------------------
    def to_dict(self):
        """Return a JSON-serializable dictionary representation."""
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
            date=data.get("date", ""),
            description=data.get("description", ""),
            amount=data.get("amount", 0),
            category=data.get("category", ""),
            ttype=data.get("type", Transaction.EXPENSE),
            transaction_id=data.get("id"),
        )
    def signed_amount(self):
        """Return the amount with sign applied (negative for expenses)."""
        return self.amount if self.type == Transaction.INCOME else -self.amount
    def __repr__(self):
        return (f"Transaction(id={self.id!r}, date={self.date!r}, "
                f"description={self.description!r}, amount={self.amount!r}, "
                f"category={self.category!r}, type={self.type!r})")
class Category:
    """Predefined categories for expenses and income."""
    EXPENSE_CATEGORIES = [
        "Housing", "Food", "Transportation", "Utilities",
        "Entertainment", "Healthcare", "Shopping", "Education",
        "Travel", "Other",
    ]
    INCOME_CATEGORIES = [
        "Salary", "Freelance", "Investments", "Gifts", "Refunds", "Other",
    ]
    @staticmethod
    def get_categories(ttype):
        """Return the category list matching the given transaction type."""
        if ttype == Transaction.INCOME:
            return list(Category.INCOME_CATEGORIES)
        return list(Category.EXPENSE_CATEGORIES)