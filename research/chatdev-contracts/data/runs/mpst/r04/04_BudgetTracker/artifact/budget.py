'''
budget.py
Defines the Budget model representing a monthly spending limit for
a specific expense category, with helpers to compare against actual
spending.
'''
from transaction import Transaction
class Budget:
    """A monthly spending cap for one expense category."""
    def __init__(self, category, monthly_limit):
        if monthly_limit < 0:
            raise ValueError("Budget limit cannot be negative.")
        self.category = category.strip().title() if category else "Uncategorized"
        self.monthly_limit = round(float(monthly_limit), 2)
    def spent(self, transactions, year, month):
        """Sum of expenses in this category for the given year/month."""
        key = f"{year:04d}-{month:02d}"
        total = sum(
            t.amount for t in transactions
            if t.type == Transaction.TYPE_EXPENSE
            and t.category == self.category
            and t.month == key
        )
        return round(total, 2)
    def remaining(self, transactions, year, month):
        """Budget limit minus spending (may be negative if overspent)."""
        return round(self.monthly_limit - self.spent(transactions, year, month), 2)
    def percent_used(self, transactions, year, month):
        """Percentage of the budget consumed, capped at 999 for safety."""
        spent = self.spent(transactions, year, month)
        if self.monthly_limit <= 0:
            return 100.0 if spent > 0 else 0.0
        return round(min(spent / self.monthly_limit * 100.0, 999.0), 1)
    def status_symbol(self, transactions, year, month):
        """Return a status marker: OK / WARN / OVER based on usage."""
        pct = self.percent_used(transactions, year, month)
        if pct >= 100:
            return "OVER"
        if pct >= 80:
            return "WARN"
        return "OK"
    def to_dict(self):
        return {"category": self.category, "monthly_limit": self.monthly_limit}
    @classmethod
    def from_dict(cls, data):
        return cls(data.get("category", "Uncategorized"),
                   data.get("monthly_limit", 0.0))
    def __str__(self):
        return f"{self.category}: ${self.monthly_limit:.2f}/month"