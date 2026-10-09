'''
tracker.py
Core business logic for the Budget Tracker: manages transactions,
savings goals, and monthly budgets, and persists everything through
the DataStorage layer. All figures are rounded to cents.
'''
from collections import defaultdict
from datetime import datetime
from models import Transaction, SavingsGoal, Budget
from storage import DataStorage
class BudgetTracker:
    """Central manager for transactions, savings goals, and monthly budgets."""
    def __init__(self, storage=None):
        """Load existing data (or start fresh) through the storage layer."""
        self.storage = storage if storage else DataStorage()
        data = self.storage.load()
        self.transactions = [Transaction.from_dict(t) for t in data["transactions"]]
        self.savings_goals = [SavingsGoal.from_dict(g) for g in data["savings_goals"]]
        self.budgets = [Budget.from_dict(b) for b in data["budgets"]]
    # ------------------------------------------------------------------
    # Persistence
    # ------------------------------------------------------------------
    def save(self):
        """Persist all current data through the storage layer."""
        self.storage.save({
            "transactions": [t.to_dict() for t in self.transactions],
            "savings_goals": [g.to_dict() for g in self.savings_goals],
            "budgets": [b.to_dict() for b in self.budgets],
        })
    # ------------------------------------------------------------------
    # Transactions
    # ------------------------------------------------------------------
    def add_transaction(self, amount, category, description="", date=None,
                        transaction_type=Transaction.EXPENSE):
        """Create and store a new transaction; returns the Transaction."""
        t = Transaction(amount, category, description, date, transaction_type)
        self.transactions.append(t)
        return t
    def find_transaction(self, tid_prefix):
        """Find a transaction by an id prefix; None if zero or ambiguous."""
        matches = [t for t in self.transactions if t.id.startswith(tid_prefix)]
        return matches[0] if len(matches) == 1 else None
    def edit_transaction(self, tid, amount=None, category=None,
                         description=None, date=None, transaction_type=None):
        """Update the given fields of a transaction; True on success."""
        t = self.find_transaction(tid)
        if not t:
            return False
        if amount is not None:
            t.amount = round(float(amount), 2)
        if category is not None:
            t.category = category
        if description is not None:
            t.description = description
        if date is not None:
            t.date = date
        if transaction_type is not None:
            t.type = transaction_type
        return True
    def delete_transaction(self, tid):
        """Remove the transaction with the given id; True on success."""
        t = self.find_transaction(tid)
        if not t:
            return False
        self.transactions.remove(t)
        return True
    def get_transactions(self, month=None, transaction_type=None, category=None):
        """Return transactions filtered by month, type, and/or category."""
        result = self.transactions
        if month:
            result = [t for t in result if t.date.startswith(month)]
        if transaction_type:
            result = [t for t in result if t.type == transaction_type]
        if category:
            result = [t for t in result if t.category.lower() == category.lower()]
        return sorted(result, key=lambda t: t.date)
    def total_income(self, month=None):
        """Sum of income transactions, optionally limited to one month."""
        return round(sum(t.amount for t in
                         self.get_transactions(month, Transaction.INCOME)), 2)
    def total_expenses(self, month=None):
        """Sum of expense transactions, optionally limited to one month."""
        return round(sum(t.amount for t in
                         self.get_transactions(month, Transaction.EXPENSE)), 2)
    def net_savings(self, month=None):
        """Income minus expenses (all-time or for a single month)."""
        return round(self.total_income(month) - self.total_expenses(month), 2)
    def category_totals(self, month=None):
        """Return {category: expense_total} sorted by amount, descending."""
        totals = defaultdict(float)
        for t in self.get_transactions(month, Transaction.EXPENSE):
            totals[t.category] += t.amount
        return dict(sorted(totals.items(), key=lambda kv: kv[1], reverse=True))
    def available_months(self):
        """Return all 'YYYY-MM' months that contain at least one transaction."""
        return sorted({t.date[:7] for t in self.transactions})
    def monthly_totals(self, num_months=6):
        """Return {month: {'income': x, 'expenses': y}} for the last N months."""
        months = set(self.available_months())
        months.add(datetime.now().strftime("%Y-%m"))
        recent = sorted(months)[-num_months:]
        result = {}
        for m in recent:
            result[m] = {
                "income": round(self.total_income(m), 2),
                "expenses": round(self.total_expenses(m), 2),
            }
        return result
    # ------------------------------------------------------------------
    # Budgets
    # ------------------------------------------------------------------
    def set_budget(self, category, monthly_limit):
        """Create or update the monthly budget for a category."""
        for b in self.budgets:
            if b.category.lower() == category.lower():
                b.monthly_limit = round(float(monthly_limit), 2)
                return b
        b = Budget(category, monthly_limit)
        self.budgets.append(b)
        return b
    def budget_status(self, month=None):
        """Return per-budget dicts (limit, spent, percent, over) for a month."""
        if month is None:
            month = datetime.now().strftime("%Y-%m")
        status = []
        for b in self.budgets:
            spent = round(sum(t.amount for t in self.get_transactions(
                month, Transaction.EXPENSE, b.category)), 2)
            if b.monthly_limit > 0:
                percent = spent / b.monthly_limit * 100
            else:
                percent = 100.0 if spent > 0 else 0.0
            status.append({
                "category": b.category,
                "limit": b.monthly_limit,
                "spent": spent,
                "percent": round(percent, 1),
                "over": spent > b.monthly_limit,
            })
        return status
    # ------------------------------------------------------------------
    # Savings goals
    # ------------------------------------------------------------------
    def add_savings_goal(self, name, target_amount, deadline=None):
        """Create a new savings goal and store it."""
        g = SavingsGoal(name, target_amount, deadline=deadline)
        self.savings_goals.append(g)
        return g
    def find_savings_goal(self, gid_prefix):
        """Find a savings goal by an id prefix; None if zero or ambiguous."""
        matches = [g for g in self.savings_goals if g.id.startswith(gid_prefix)]
        return matches[0] if len(matches) == 1 else None
    def contribute_to_goal(self, gid, amount):
        """Add money to a savings goal; returns the goal or None."""
        g = self.find_savings_goal(gid)
        if g:
            g.contribute(amount)
        return g
    def withdraw_from_goal(self, gid, amount):
        """Remove money from a savings goal; returns the goal or None."""
        g = self.find_savings_goal(gid)
        if g:
            g.withdraw(amount)
        return g
    def delete_savings_goal(self, gid):
        """Delete a savings goal; True on success."""
        g = self.find_savings_goal(gid)
        if not g:
            return False
        self.savings_goals.remove(g)
        return True