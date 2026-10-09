'''
analytics.py
Pure calculation helpers used by the GUI and chart modules. All functions
operate on lists of Transaction / SavingsGoal objects and never mutate them.
'''
from collections import defaultdict
from datetime import datetime
from models import EXPENSE, INCOME, Transaction
def format_currency(value):
    """Format a number as a currency string, e.g. -1234.50 -> '-$1,234.50'."""
    sign = "-" if value < 0 else ""
    return f"{sign}${abs(value):,.2f}"
def total_by_type(transactions, t_type):
    return sum(t.amount for t in transactions if t.type == t_type)
def total_income(transactions):
    return total_by_type(transactions, INCOME)
def total_expenses(transactions):
    return total_by_type(transactions, EXPENSE)
def net_savings(transactions):
    return total_income(transactions) - total_expenses(transactions)
def savings_rate(transactions):
    """Percentage of income that was kept as savings (0-100)."""
    income = total_income(transactions)
    if income <= 0:
        return 0.0
    return max(net_savings(transactions) / income * 100.0, 0.0)
def by_category(transactions, t_type):
    """Return {category: total} for the given transaction type, sorted desc."""
    totals = defaultdict(float)
    for t in transactions:
        if t.type == t_type:
            totals[t.category] += t.amount
    return dict(sorted(totals.items(), key=lambda kv: kv[1], reverse=True))
def expenses_by_category(transactions):
    return by_category(transactions, EXPENSE)
def income_by_category(transactions):
    return by_category(transactions, INCOME)
def month_key(date_str):
    """'2024-05-17' -> '2024-05'."""
    return date_str[:7]
def available_months(transactions):
    """Sorted list of 'YYYY-MM' strings present in the data (newest first)."""
    months = {month_key(t.date) for t in transactions}
    return sorted(months, reverse=True)
def filter_by_month(transactions, month):
    """Return transactions belonging to 'YYYY-MM'. None means all."""
    if month in (None, "", "All"):
        return list(transactions)
    return [t for t in transactions if month_key(t.date) == month]
def filter_by_type(transactions, t_type):
    if t_type in (None, "", "All"):
        return list(transactions)
    return [t for t in transactions if t.type == t_type]
def filter_by_category(transactions, category):
    if category in (None, "", "All"):
        return list(transactions)
    return [t for t in transactions if t.category == category]
def monthly_summary(transactions):
    """
    Return {'YYYY-MM': {'income': x, 'expense': y, 'savings': x-y}}
    sorted chronologically.
    """
    summary = defaultdict(lambda: {"income": 0.0, "expense": 0.0, "savings": 0.0})
    for t in transactions:
        bucket = summary[month_key(t.date)]
        if t.type == INCOME:
            bucket["income"] += t.amount
        else:
            bucket["expense"] += t.amount
        bucket["savings"] = bucket["income"] - bucket["expense"]
    return dict(sorted(summary.items()))
def cumulative_savings(transactions):
    """
    Return a chronologically sorted list of (date, running_balance) tuples,
    starting from the first transaction.
    """
    ordered = sorted(transactions, key=lambda t: (t.date, t.id))
    points = []
    balance = 0.0
    for t in ordered:
        balance += t.signed_amount
        points.append((t.date, balance))
    return points
def top_expense_categories(transactions, n=5):
    items = list(expenses_by_category(transactions).items())
    return items[:n]
def largest_expenses(transactions, n=5):
    expenses = [t for t in transactions if t.type == EXPENSE]
    return sorted(expenses, key=lambda t: t.amount, reverse=True)[:n]
def goals_overview(goals):
    """Aggregate stats for savings goals."""
    total_target = sum(g.target_amount for g in goals)
    total_saved = sum(g.saved_amount for g in goals)
    completed = sum(1 for g in goals if g.is_complete)
    overall = (total_saved / total_target * 100.0) if total_target > 0 else 0.0
    return {
        "total_target": total_target,
        "total_saved": total_saved,
        "completed": completed,
        "overall_percent": overall,
    }