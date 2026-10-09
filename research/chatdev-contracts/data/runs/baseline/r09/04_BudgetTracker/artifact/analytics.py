'''
analytics.py
Calculation helpers for the Budget Tracker application.
BudgetAnalytics consumes lists of Transaction objects and produces
aggregates: totals, category breakdowns, monthly summaries, budget
status, and savings-trend data used by the charts.
'''
from collections import defaultdict
from datetime import datetime
from models import DATE_FORMAT
class BudgetAnalytics:
    """Computes summary statistics from a list of transactions."""
    def __init__(self, transactions, budget_limits=None):
        self.transactions = transactions
        self.budget_limits = budget_limits or {}
    def income_transactions(self):
        return [t for t in self.transactions if t.type == "income"]
    def expense_transactions(self):
        return [t for t in self.transactions if t.type == "expense"]
    def total_income(self):
        return round(sum(t.amount for t in self.income_transactions()), 2)
    def total_expenses(self):
        return round(sum(t.amount for t in self.expense_transactions()), 2)
    def net_savings(self):
        return round(self.total_income() - self.total_expenses(), 2)
    def savings_rate(self):
        income = self.total_income()
        if income <= 0:
            return 0.0
        return round(max(0.0, self.net_savings()) / income * 100.0, 1)
    def expenses_by_category(self):
        """Return {category: total_spent} sorted from largest to smallest."""
        totals = defaultdict(float)
        for t in self.expense_transactions():
            totals[t.category] += t.amount
        return dict(sorted(totals.items(), key=lambda kv: kv[1], reverse=True))
    def monthly_summary(self):
        """Return {('YYYY-MM'): {'income': x, 'expenses': y, 'net': z}} sorted chronologically."""
        summary = defaultdict(lambda: {"income": 0.0, "expenses": 0.0})
        for t in self.transactions:
            month = t.date[:7]  # "YYYY-MM"
            if t.type == "income":
                summary[month]["income"] += t.amount
            else:
                summary[month]["expenses"] += t.amount
        result = {}
        for month in sorted(summary):
            income = round(summary[month]["income"], 2)
            expenses = round(summary[month]["expenses"], 2)
            result[month] = {"income": income, "expenses": expenses, "net": round(income - expenses, 2)}
        return result
    def cumulative_savings_trend(self):
        """Return ([month_labels], [cumulative_net_savings]) for the line chart."""
        summary = self.monthly_summary()
        labels = list(summary.keys())
        values = []
        running = 0.0
        for month in labels:
            running += summary[month]["net"]
            values.append(round(running, 2))
        return labels, values
    def budget_status(self):
        """Compare current-month spending per category against budget limits.
        Returns list of dicts: category, spent, limit, remaining, pct."""
        current_month = datetime.now().strftime("%Y-%m")
        spent = defaultdict(float)
        for t in self.expense_transactions():
            if t.date[:7] == current_month:
                spent[t.category] += t.amount
        rows = []
        for category, limit in self.budget_limits.items():
            s = round(spent.get(category, 0.0), 2)
            rows.append({
                "category": category,
                "spent": s,
                "limit": limit,
                "remaining": round(limit - s, 2),
                "pct": round(s / limit * 100.0, 1) if limit > 0 else 0.0,
            })
        return rows
    def recent_transactions(self, n=8):
        """Return the n most recent transactions sorted by date descending."""
        return sorted(self.transactions, key=lambda t: t.date, reverse=True)[:n]