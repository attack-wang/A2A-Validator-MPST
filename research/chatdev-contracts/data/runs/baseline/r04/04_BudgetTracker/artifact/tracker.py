'''
tracker.py
Core business logic for the Budget Tracker application.
Classes:
    BudgetTracker: Manages transactions and category budgets, provides
        CRUD operations, filtering, summaries, and analytics used by the GUI.
'''
from datetime import datetime
from models import Transaction, Category
from storage import JSONStorage
class BudgetTracker:
    """Manages all financial data and derived statistics."""
    def __init__(self, storage=None):
        """
        Initialize the tracker and load any previously saved data.
        Args:
            storage (JSONStorage, optional): Custom storage handler.
        """
        self.storage = storage if storage is not None else JSONStorage()
        data = self.storage.load()
        self.transactions = []
        for record in data.get("transactions", []):
            try:
                self.transactions.append(Transaction.from_dict(record))
            except ValueError:
                continue  # skip corrupted records
        self.budgets = {str(k): float(v) for k, v in data.get("budgets", {}).items()}
    # ------------------------------------------------------------------ #
    # Persistence
    # ------------------------------------------------------------------ #
    def _persist(self):
        """Write the current state to storage."""
        data = {
            "transactions": [t.to_dict() for t in self.transactions],
            "budgets": self.budgets,
        }
        self.storage.save(data)
    # ------------------------------------------------------------------ #
    # Transaction CRUD
    # ------------------------------------------------------------------ #
    def add_transaction(self, date, description, amount, category, ttype):
        """Create, store, and return a new Transaction."""
        transaction = Transaction(date, description, amount, category, ttype)
        self.transactions.append(transaction)
        self._persist()
        return transaction
    def get_transaction(self, transaction_id):
        """Return the Transaction with the given id, or None."""
        for transaction in self.transactions:
            if transaction.id == transaction_id:
                return transaction
        return None
    def update_transaction(self, transaction_id, date, description, amount, category, ttype):
        """Update an existing transaction; returns True on success."""
        transaction = self.get_transaction(transaction_id)
        if transaction is None:
            return False
        # Validate through a temporary instance before applying.
        updated = Transaction(date, description, amount, category, ttype, transaction_id=transaction_id)
        transaction.date = updated.date
        transaction.description = updated.description
        transaction.amount = updated.amount
        transaction.category = updated.category
        transaction.type = updated.type
        self._persist()
        return True
    def delete_transaction(self, transaction_id):
        """Remove a transaction; returns True if it existed."""
        original_count = len(self.transactions)
        self.transactions = [t for t in self.transactions if t.id != transaction_id]
        removed = len(self.transactions) < original_count
        if removed:
            self._persist()
        return removed
    def get_all_transactions(self):
        """Return all transactions sorted by date (newest first)."""
        return sorted(self.transactions, key=lambda t: (t.date, t.id), reverse=True)
    # ------------------------------------------------------------------ #
    # Filtering
    # ------------------------------------------------------------------ #
    def get_transactions_by_month(self, year, month):
        """Return transactions falling in the given year/month."""
        prefix = f"{year:04d}-{month:02d}"
        return [t for t in self.transactions if t.date.startswith(prefix)]
    def get_available_months(self):
        """Return sorted list of (year, month) tuples present in the data."""
        months = set()
        for transaction in self.transactions:
            try:
                parsed = datetime.strptime(transaction.date, Transaction.DATE_FORMAT)
                months.add((parsed.year, parsed.month))
            except ValueError:
                continue
        return sorted(months)
    # ------------------------------------------------------------------ #
    # Summaries and analytics
    # ------------------------------------------------------------------ #
    @staticmethod
    def _sum_by_type(transactions, ttype):
        return sum(t.amount for t in transactions if t.type == ttype)
    def get_total_income(self, transactions=None):
        """Total income across the given (or all) transactions."""
        transactions = self.transactions if transactions is None else transactions
        return round(self._sum_by_type(transactions, Transaction.INCOME), 2)
    def get_total_expenses(self, transactions=None):
        """Total expenses across the given (or all) transactions."""
        transactions = self.transactions if transactions is None else transactions
        return round(self._sum_by_type(transactions, Transaction.EXPENSE), 2)
    def get_savings(self, transactions=None):
        """Income minus expenses for the given (or all) transactions."""
        return round(self.get_total_income(transactions) - self.get_total_expenses(transactions), 2)
    def get_category_breakdown(self, transactions=None, ttype=Transaction.EXPENSE):
        """
        Return {category: total_amount} for transactions of the given type,
        sorted from largest to smallest.
        """
        transactions = self.transactions if transactions is None else transactions
        breakdown = {}
        for transaction in transactions:
            if transaction.type == ttype:
                breakdown[transaction.category] = breakdown.get(transaction.category, 0.0) + transaction.amount
        return dict(sorted(breakdown.items(), key=lambda item: item[1], reverse=True))
    def get_monthly_summary(self):
        """
        Return a list of dicts, one per month with data:
            {'year', 'month', 'label', 'income', 'expenses', 'savings'}
        sorted chronologically.
        """
        summary = {}
        for transaction in self.transactions:
            try:
                parsed = datetime.strptime(transaction.date, Transaction.DATE_FORMAT)
            except ValueError:
                continue
            key = (parsed.year, parsed.month)
            entry = summary.setdefault(key, {"income": 0.0, "expenses": 0.0})
            if transaction.type == Transaction.INCOME:
                entry["income"] += transaction.amount
            else:
                entry["expenses"] += transaction.amount
        result = []
        for (year, month) in sorted(summary.keys()):
            entry = summary[(year, month)]
            result.append({
                "year": year,
                "month": month,
                "label": f"{year}-{month:02d}",
                "income": round(entry["income"], 2),
                "expenses": round(entry["expenses"], 2),
                "savings": round(entry["income"] - entry["expenses"], 2),
            })
        return result
    def get_savings_trend(self):
        """
        Return cumulative savings over time as (labels, cumulative_values),
        one point per month with data, sorted chronologically.
        """
        monthly = self.get_monthly_summary()
        labels = [entry["label"] for entry in monthly]
        cumulative = []
        running_total = 0.0
        for entry in monthly:
            running_total += entry["savings"]
            cumulative.append(round(running_total, 2))
        return labels, cumulative
    # ------------------------------------------------------------------ #
    # Budgets
    # ------------------------------------------------------------------ #
    def set_budget(self, category, amount):
        """Set (or update) the monthly budget for a category."""
        category = str(category).strip()
        if not category:
            raise ValueError("Category cannot be empty.")
        amount = float(amount)
        if amount <= 0:
            raise ValueError("Budget must be greater than zero.")
        self.budgets[category] = round(amount, 2)
        self._persist()
    def remove_budget(self, category):
        """Delete the budget for a category; returns True if it existed."""
        if str(category) in self.budgets:
            del self.budgets[str(category)]
            self._persist()
            return True
        return False
    def get_budget_status(self, year, month):
        """
        Return budget progress for the given month as a list of dicts:
            {'category', 'budget', 'spent', 'remaining', 'percent_used'}
        sorted by percent used (descending).
        """
        month_transactions = self.get_transactions_by_month(year, month)
        expenses_by_category = self.get_category_breakdown(month_transactions, Transaction.EXPENSE)
        status = []
        for category, budget in self.budgets.items():
            spent = round(expenses_by_category.get(category, 0.0), 2)
            remaining = round(budget - spent, 2)
            percent = round((spent / budget) * 100.0, 1) if budget > 0 else 0.0
            status.append({
                "category": category,
                "budget": budget,
                "spent": spent,
                "remaining": remaining,
                "percent_used": percent,
            })
        status.sort(key=lambda item: item["percent_used"], reverse=True)
        return status