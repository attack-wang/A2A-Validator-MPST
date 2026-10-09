'''
analytics.py
Pure calculation helpers used by the GUI: totals, category breakdowns,
monthly summaries, budget status and savings progress.
All functions are side-effect free so they are easy to test and reuse.
'''
from datetime import datetime
def current_month():
    """Return the current month as 'YYYY-MM'."""
    return datetime.now().strftime("%Y-%m")
def available_months(transactions):
    """Sorted list of months (YYYY-MM) that appear in the transactions."""
    return sorted({t.month for t in transactions})
def filter_by_month(transactions, month=None):
    """Return only the transactions of the given month (all if month is None)."""
    if month in (None, "", "All"):
        return list(transactions)
    return [t for t in transactions if t.month == month]
def total_by_kind(transactions, kind, month=None):
    """Sum of amounts for the given kind ('expense' or 'income'), optionally per month."""
    return round(sum(t.amount for t in filter_by_month(transactions, month) if t.kind == kind), 2)
def total_expenses(transactions, month=None):
    return total_by_kind(transactions, "expense", month)
def total_income(transactions, month=None):
    return total_by_kind(transactions, "income", month)
def net_savings(transactions, month=None):
    """Income minus expenses for the period."""
    return round(total_income(transactions, month) - total_expenses(transactions, month), 2)
def expenses_by_category(transactions, month=None):
    """{category: total} for expenses, sorted from highest to lowest."""
    totals = {}
    for t in filter_by_month(transactions, month):
        if t.kind != "expense":
            continue
        totals[t.category] = round(totals.get(t.category, 0.0) + t.amount, 2)
    return dict(sorted(totals.items(), key=lambda item: item[1], reverse=True))
def expenses_by_month(transactions):
    """{month: total expenses} sorted chronologically."""
    totals = {}
    for t in transactions:
        if t.kind != "expense":
            continue
        totals[t.month] = round(totals.get(t.month, 0.0) + t.amount, 2)
    return dict(sorted(totals.items()))
def net_by_month(transactions):
    """{month: net savings (income - expenses)} sorted chronologically."""
    result = {}
    for t in transactions:
        sign = 1 if t.kind == "income" else -1
        result[t.month] = round(result.get(t.month, 0.0) + sign * t.amount, 2)
    return dict(sorted(result.items()))
def budget_status(budget, transactions, month):
    """
    Summarise budget usage for one month.
    Returns a dict with:
        month, income, spent, net, limit, remaining,
        categories: list of dicts {category, spent, limit, remaining, over}
    """
    spent = total_expenses(transactions, month)
    income = total_income(transactions, month)
    limit = budget.monthly_limit
    remaining = round(limit - spent, 2) if limit > 0 else None
    by_category = expenses_by_category(transactions, month)
    categories = []
    for category, cat_spent in by_category.items():
        cat_limit = budget.limit_for(category)
        categories.append({
            "category": category,
            "spent": cat_spent,
            "limit": cat_limit,
            "remaining": round(cat_limit - cat_spent, 2) if cat_limit else None,
            "over": bool(cat_limit and cat_spent > cat_limit),
        })
    return {
        "month": month,
        "income": income,
        "spent": spent,
        "net": round(income - spent, 2),
        "limit": limit,
        "remaining": remaining,
        "categories": categories,
    }
def savings_summary(goals):
    """(total_target, total_saved, overall_progress_ratio) across all goals."""
    total_target = round(sum(g.target_amount for g in goals), 2)
    total_saved = round(sum(g.saved_amount for g in goals), 2)
    ratio = (total_saved / total_target) if total_target > 0 else 0.0
    return total_target, total_saved, min(1.0, ratio)