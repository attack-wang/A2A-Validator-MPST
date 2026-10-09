'''
transaction.py
Defines the Transaction model used to record individual financial
activities: expenses, income, savings deposits and savings withdrawals.
'''
import uuid
from datetime import datetime
class Transaction:
    """Represents a single financial transaction."""
    TYPE_EXPENSE = "expense"
    TYPE_INCOME = "income"
    TYPE_SAVINGS = "savings"           # deposit into savings
    TYPE_SAVINGS_OUT = "savings_out"   # withdrawal from savings
    VALID_TYPES = (TYPE_EXPENSE, TYPE_INCOME, TYPE_SAVINGS, TYPE_SAVINGS_OUT)
    def __init__(self, amount, category, description="", date=None,
                 t_type=TYPE_EXPENSE, t_id=None):
        if amount <= 0:
            raise ValueError("Transaction amount must be positive.")
        if t_type not in Transaction.VALID_TYPES:
            raise ValueError(f"Invalid transaction type: {t_type}")
        self.id = t_id if t_id else uuid.uuid4().hex[:8]
        self.amount = round(float(amount), 2)
        self.category = category.strip().title() if category else "Uncategorized"
        self.description = description.strip()
        self.date = date if date else datetime.now().strftime("%Y-%m-%d")
        self.type = t_type
    @property
    def month(self):
        """Return the 'YYYY-MM' key for grouping by month."""
        return self.date[:7]
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
            amount=data.get("amount", 0.0),
            category=data.get("category", "Uncategorized"),
            description=data.get("description", ""),
            date=data.get("date"),
            t_type=data.get("type", cls.TYPE_EXPENSE),
            t_id=data.get("id"),
        )
    def __str__(self):
        sign = "-" if self.type in (Transaction.TYPE_EXPENSE,
                                    Transaction.TYPE_SAVINGS_OUT) else "+"
        return (f"[{self.id}] {self.date} | {self.type.upper():11} | "
                f"{self.category:<15} | {sign}${self.amount:>10.2f} | {self.description}")