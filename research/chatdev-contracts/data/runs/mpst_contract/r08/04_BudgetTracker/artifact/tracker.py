from datetime import datetime

import storage
from models import Budget, Transaction


class BudgetTracker:
    def __init__(self):
        self.data = storage.load()
        self.transactions = [Transaction.from_dict(t) for t in self.data["transactions"]]
        self.budget = Budget.from_dict(self.data["budget"])

    def _persist(self):
        self.data["transactions"] = [t.to_dict() for t in self.transactions]
        self.data["budget"] = self.budget.to_dict()
        storage.save(self.data)

    def add_transaction(self, ttype, category, description, amount, date=None):
        date = date or datetime.now().strftime("%Y-%m-%d")
        t = Transaction(date, category, description, round(float(amount), 2), ttype)
        self.transactions.append(t)
        self._persist()
        return t

    def remove_transaction(self, index):
        if 0 <= index < len(self.transactions):
            removed = self.transactions.pop(index)
            self._persist()
            return removed
        return None

    def set_budget(self, income_goal=None, savings_goal=None, category_limits=None):
        if income_goal is not None:
            self.budget.monthly_income_goal = float(income_goal)
        if savings_goal is not None:
            self.budget.savings_goal = float(savings_goal)
        if category_limits is not None:
            self.budget.category_limits = dict(category_limits)
        self._persist()

    def totals(self, month=None):
        income = sum(
            t.amount for t in self.transactions
            if t.ttype == "income" and (month is None or t.date.startswith(month))
        )
        expenses = sum(
            t.amount for t in self.transactions
            if t.ttype == "expense" and (month is None or t.date.startswith(month))
        )
        return income, expenses, income - expenses

    def category_breakdown(self, month=None):
        breakdown = {}
        for t in self.transactions:
            if t.ttype == "expense" and (month is None or t.date.startswith(month)):
                breakdown[t.category] = breakdown.get(t.category, 0.0) + t.amount
        return breakdown

    def monthly_report(self, month):
        income, expenses, savings = self.totals(month)
        lines = [
            f"=== Report for {month} ===",
            f"  Income:   ${income:.2f}",
            f"  Expenses: ${expenses:.2f}",
            f"  Savings:  ${savings:.2f}",
        ]
        if self.budget.savings_goal > 0:
            pct = max(0.0, min(100.0, savings / self.budget.savings_goal * 100))
            lines.append(
                f"  Savings goal: ${self.budget.savings_goal:.2f} ({pct:.0f}% reached)"
            )
        if self.budget.category_limits:
            breakdown = self.category_breakdown(month)
            lines.append("  Category limits:")
            for cat, limit in self.budget.category_limits.items():
                spent = breakdown.get(cat, 0.0)
                status = "OK" if spent <= limit else "OVER"
                lines.append(
                    f"    {cat}: spent ${spent:.2f} / limit ${limit:.2f} [{status}]"
                )
        return "\n".join(lines)