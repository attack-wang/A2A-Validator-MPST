'''
analytics.py
Financial analysis helpers for the Budget Tracker application.
``BudgetAnalyzer`` groups pure calculation functions used by the GUI
and the chart module. Every method is a ``staticmethod`` so the logic
can be reused without instantiating the class.
'''
from collections import defaultdict
from datetime import datetime
from models import format_currency
class BudgetAnalyzer:
    """Pure calculation helpers over lists of transactions."""
    # ------------------------------------------------------------------
    # Totals
    # ------------------------------------------------------------------
    @staticmethod
    def total_income(transactions):
        """Sum of every income transaction."""
        return sum(t.amount for t in transactions
                   if t.transaction_type == "income")
    @staticmethod
    def total_expenses(transactions):
        """Sum of every expense transaction."""
        return sum(t.amount for t in transactions
                   if t.transaction_type == "expense")
    @staticmethod
    def net_savings(transactions):
        """Income minus expenses; may be negative when overspending."""
        return BudgetAnalyzer.total_income(transactions) - \
            BudgetAnalyzer.total_expenses(transactions)
    @staticmethod
    def savings_rate(transactions):
        """Net savings as a percentage of income (0 when no income)."""
        income = BudgetAnalyzer.total_income(transactions)
        if income <= 0:
            return 0.0
        return (BudgetAnalyzer.net_savings(transactions) / income) * 100.0
    # ------------------------------------------------------------------
    # Grouping
    # ------------------------------------------------------------------
    @staticmethod
    def expenses_by_category(transactions):
        """Return ``{category: total}`` for expense transactions."""
        totals = defaultdict(float)
        for t in transactions:
            if t.transaction_type == "expense":
                totals[t.category] += t.amount
        return dict(sorted(totals.items(), key=lambda kv: kv[1], reverse=True))
    @staticmethod
    def income_by_category(transactions):
        """Return ``{category: total}`` for income transactions."""
        totals = defaultdict(float)
        for t in transactions:
            if t.transaction_type == "income":
                totals[t.category] += t.amount
        return dict(sorted(totals.items(), key=lambda kv: kv[1], reverse=True))
    @staticmethod
    def monthly_summary(transactions):
        """Return ``{YYYY-MM: {"income": x, "expense": y, "net": z}}``."""
        summary = defaultdict(lambda: {"income": 0.0, "expense": 0.0})
        for t in transactions:
            bucket = summary[t.month_key]
            bucket[t.transaction_type] += t.amount
        result = {}
        for month in sorted(summary):
            income = summary[month]["income"]
            expense = summary[month]["expense"]
            result[month] = {
                "income": income,
                "expense": expense,
                "net": income - expense,
            }
        return result
    @staticmethod
    def savings_over_time(transactions):
        """Cumulative net savings ordered by transaction date.
        Returns a list of ``(YYYY-MM, cumulative_net)`` tuples, one per
        month that has at least one transaction.
        """
        monthly = BudgetAnalyzer.monthly_summary(transactions)
        cumulative = 0.0
        timeline = []
        for month in sorted(monthly):
            cumulative += monthly[month]["net"]
            timeline.append((month, cumulative))
        return timeline
    @staticmethod
    def available_months(transactions):
        """Sorted list of ``YYYY-MM`` strings present in the data."""
        return sorted({t.month_key for t in transactions})
    # ------------------------------------------------------------------
    # Budget tracking
    # ------------------------------------------------------------------
    @staticmethod
    def spent_in_month(transactions, category, month_key):
        """Total expenses for one category within one ``YYYY-MM`` month."""
        return sum(
            t.amount for t in transactions
            if t.transaction_type == "expense"
            and t.category == category
            and t.month_key == month_key
        )
    @staticmethod
    def budget_usage(transactions, budgets, month_key=None):
        """Budget progress rows.
        When ``month_key`` is None the *current* month is used. Returns
        a list of dictionaries with the category, limit, spent amount,
        remaining amount and a usage percentage capped at 999%.
        """
        if month_key is None:
            month_key = datetime.now().strftime("%Y-%m")
        rows = []
        for budget in budgets:
            spent = BudgetAnalyzer.spent_in_month(
                transactions, budget.category, month_key)
            remaining = budget.monthly_limit - spent
            if budget.monthly_limit > 0:
                percent = min(spent / budget.monthly_limit * 100.0, 999.0)
            else:
                percent = 0.0
            rows.append({
                "category": budget.category,
                "limit": budget.monthly_limit,
                "spent": spent,
                "remaining": remaining,
                "percent": percent,
                "over_budget": spent > budget.monthly_limit,
            })
        return rows
    # ------------------------------------------------------------------
    # Formatting helpers
    # ------------------------------------------------------------------
    @staticmethod
    def format_summary(transactions):
        """Human readable multi-line summary of the whole data set."""
        income = BudgetAnalyzer.total_income(transactions)
        expenses = BudgetAnalyzer.total_expenses(transactions)
        net = BudgetAnalyzer.net_savings(transactions)
        rate = BudgetAnalyzer.savings_rate(transactions)
        return (
            "Total Income:      {}\n"
            "Total Expenses:    {}\n"
            "Net Savings:       {}\n"
            "Savings Rate:      {:.1f}%"
        ).format(format_currency(income), format_currency(expenses),
                 format_currency(net), rate)