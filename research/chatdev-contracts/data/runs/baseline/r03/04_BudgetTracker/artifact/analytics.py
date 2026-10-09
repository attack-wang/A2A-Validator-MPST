'''
analytics.py
Pure calculation helpers used by the GUI to summarise budget data.
All functions are stateless: they take lists of Transaction / SavingsGoal
objects (or budget dicts) and return plain Python data structures.
'''
from collections import defaultdict
from datetime import date
from models import Transaction
def _parse_month(date_str):
    """Return 'YYYY-MM' for an ISO date string, or None if unparseable."""
    try:
        return date_str[:7]
    except (TypeError, AttributeError):
        return None
def total_income(transactions):
    return round(sum(t.amount for t in transactions if t.type == Transaction.INCOME), 2)
def total_expenses(transactions):
    return round(sum(t.amount for t in transactions if t.type == Transaction.EXPENSE), 2)
def spending_by_category(transactions):
    """Return {category: total_expense} sorted from largest to smallest."""
    totals = defaultdict(float)
    for t in transactions:
        if t.is_expense():
            totals[t.category] += t.amount
    return dict(sorted(totals.items(), key=lambda kv: kv[1], reverse=True))
def monthly_totals(transactions, last_n_months=6):
    """Return a list of (month, income, expense) tuples for the last N months."""
    income = defaultdict(float)
    expense = defaultdict(float)
    for t in transactions:
        month = _parse_month(t.date)
        if month is None:
            continue
        if t.type == Transaction.INCOME:
            income[month] += t.amount
        else:
            expense[month] += t.amount
    months = sorted(set(income) | set(expense), reverse=True)[:last_n_months]
    months = sorted(months)
    return [(m, round(income.get(m, 0.0), 2), round(expense.get(m, 0.0), 2)) for m in months]
def budget_usage(budgets, transactions):
    """Return rows (category, limit, spent, remaining, pct) for the current month."""
    current_month = date.today().strftime("%Y-%m")
    spent_by_cat = defaultdict(float)
    for t in transactions:
        if t.is_expense() and _parse_month(t.date) == current_month:
            spent_by_cat[t.category] += t.amount
    rows = []
    for category, limit in sorted(budgets.items()):
        spent = round(spent_by_cat.get(category, 0.0), 2)
        remaining = round(limit - spent, 2)
        pct = (spent / limit * 100.0) if limit > 0 else 0.0
        rows.append((category, limit, spent, remaining, round(pct, 1)))
    return rows
def overall_goal_progress(goals):
    """Return (saved, target, pct) across all goals, or None if no goals."""
    if not goals:
        return None
    saved = round(sum(g.saved_amount for g in goals), 2)
    target = round(sum(g.target_amount for g in goals), 2)
    pct = (saved / target * 100.0) if target > 0 else 100.0
    return saved, target, min(100.0, round(pct, 1))