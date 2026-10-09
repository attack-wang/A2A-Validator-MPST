'''
tracker.py
Core business logic for the budget tracker. Manages collections of
transactions, budgets, and savings goals, and persists changes via
the DataManager.
'''
from transaction import Transaction
from budget import Budget
from savings_goal import SavingsGoal
from data_manager import DataManager
class BudgetTracker:
    """Central controller holding all tracker state and operations."""
    def __init__(self, filepath="budget_data.json"):
        self.data_manager = DataManager(filepath)
        self.transactions = []
        self.budgets = []
        self.goals = []
        self.load()
    # ---------- persistence ----------
    def load(self):
        """Restore transactions, budgets and goals from disk."""
        data = self.data_manager.load()
        self.transactions = [Transaction.from_dict(d) for d in data["transactions"]]
        self.budgets = [Budget.from_dict(d) for d in data["budgets"]]
        self.goals = [SavingsGoal.from_dict(d) for d in data["goals"]]
    def save(self):
        """Serialize all state to disk."""
        self.data_manager.save({
            "transactions": [t.to_dict() for t in self.transactions],
            "budgets": [b.to_dict() for b in self.budgets],
            "goals": [g.to_dict() for g in self.goals],
        })
    # ---------- transactions ----------
    def add_transaction(self, amount, category, description="", date=None,
                        t_type=Transaction.TYPE_EXPENSE):
        """Create, store and persist a new transaction."""
        t = Transaction(amount, category, description, date, t_type)
        self.transactions.append(t)
        self.save()
        return t
    def delete_transaction(self, t_id):
        """Remove a transaction by ID; return True if deleted."""
        for i, t in enumerate(self.transactions):
            if t.id == t_id:
                del self.transactions[i]
                self.save()
                return True
        return False
    def find_transaction(self, t_id):
        """Return the transaction with the given ID, or None."""
        for t in self.transactions:
            if t.id == t_id:
                return t
        return None
    def transactions_for(self, year, month, t_type=None):
        """Return transactions for a month, optionally filtered by type."""
        key = f"{year:04d}-{month:02d}"
        return [t for t in self.transactions
                if t.month == key and (t_type is None or t.type == t_type)]
    # ---------- budgets ----------
    def add_budget(self, category, limit):
        """Create or replace the budget for a category."""
        b = Budget(category, limit)
        self.budgets = [x for x in self.budgets if x.category != b.category]
        self.budgets.append(b)
        self.save()
        return b
    def remove_budget(self, category):
        """Delete the budget for a category; return True if removed."""
        key = category.strip().title()
        for i, b in enumerate(self.budgets):
            if b.category == key:
                del self.budgets[i]
                self.save()
                return True
        return False
    def get_budget(self, category):
        """Return the budget for a category, or None."""
        key = category.strip().title()
        for b in self.budgets:
            if b.category == key:
                return b
        return None
    # ---------- savings goals ----------
    def add_goal(self, name, target, current=0.0):
        """Create and persist a new savings goal."""
        g = SavingsGoal(name, target, current)
        self.goals.append(g)
        self.save()
        return g
    def remove_goal(self, name):
        """Delete a goal by name; return True if removed."""
        key = name.strip().lower()
        for i, g in enumerate(self.goals):
            if g.name.lower() == key:
                del self.goals[i]
                self.save()
                return True
        return False
    def get_goal(self, name):
        """Return the goal with the given name (case-insensitive), or None."""
        key = name.strip().lower()
        for g in self.goals:
            if g.name.lower() == key:
                return g
        return None
    def deposit_to_goal(self, name, amount):
        """Deposit into a goal and record a savings transaction."""
        goal = self.get_goal(name)
        if goal:
            goal.deposit(amount)
            self.add_transaction(amount, name,
                                 f"Deposit to savings goal '{name}'",
                                 t_type=Transaction.TYPE_SAVINGS)
        return goal
    def withdraw_from_goal(self, name, amount):
        """Withdraw from a goal and record a savings_out transaction."""
        goal = self.get_goal(name)
        if goal:
            goal.withdraw(amount)  # may raise ValueError; nothing recorded
            self.add_transaction(amount, name,
                                 f"Withdrawal from savings goal '{name}'",
                                 t_type=Transaction.TYPE_SAVINGS_OUT)
        return goal
    # ---------- summaries ----------
    def monthly_summary(self, year, month):
        """Return income/expense/savings/net totals for a month."""
        key = f"{year:04d}-{month:02d}"
        income = sum(t.amount for t in self.transactions
                     if t.month == key and t.type == Transaction.TYPE_INCOME)
        expenses = sum(t.amount for t in self.transactions
                       if t.month == key and t.type == Transaction.TYPE_EXPENSE)
        deposits = sum(t.amount for t in self.transactions
                       if t.month == key and t.type == Transaction.TYPE_SAVINGS)
        withdrawals = sum(t.amount for t in self.transactions
                          if t.month == key and t.type == Transaction.TYPE_SAVINGS_OUT)
        savings = round(deposits - withdrawals, 2)
        net = round(income - expenses - savings, 2)
        return {"income": round(income, 2), "expenses": round(expenses, 2),
                "savings": savings, "net": net}
    def category_breakdown(self, year, month):
        """Return {category: total} for expenses in a month."""
        breakdown = {}
        for t in self.transactions_for(year, month, Transaction.TYPE_EXPENSE):
            breakdown[t.category] = round(breakdown.get(t.category, 0.0) + t.amount, 2)
        return breakdown