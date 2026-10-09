'''
budget_manager.py
Business-logic layer for the Budget Tracker application.
BudgetManager coordinates transactions, budgets, and savings goals,
performing all calculations (category totals, monthly summaries,
budget status, savings progress, trends) that the GUI and chart
modules consume.
'''
from collections import defaultdict
from datetime import datetime
from models import Transaction, Budget, SavingsGoal
from storage import Storage
class BudgetManager:
    """Manages all financial data and provides summary calculations."""
    def __init__(self, storage=None):
        self.storage = storage if storage else Storage()
        data = self.storage.load()
        self.transactions = [Transaction.from_dict(t) for t in data.get("transactions", [])]
        self.budgets = [Budget.from_dict(b) for b in data.get("budgets", [])]
        self.savings_goals = [SavingsGoal.from_dict(g) for g in data.get("savings_goals", [])]
    # ------------------------------------------------------------------
    # Persistence
    # ------------------------------------------------------------------
    def _persist(self):
        """Write the current state to storage."""
        data = {
            "transactions": [t.to_dict() for t in self.transactions],
            "budgets": [b.to_dict() for b in self.budgets],
            "savings_goals": [g.to_dict() for g in self.savings_goals],
        }
        self.storage.save(data)
    # ------------------------------------------------------------------
    # Transactions
    # ------------------------------------------------------------------
    def add_expense(self, amount, category, description="", date=None):
        """Record an expense and return the created Transaction."""
        txn = Transaction(amount, category, description, date, transaction_type="expense")
        self.transactions.append(txn)
        self._persist()
        return txn
    def add_income(self, amount, source, description="", date=None):
        """Record income and return the created Transaction."""
        txn = Transaction(amount, source, description, date, transaction_type="income")
        self.transactions.append(txn)
        self._persist()
        return txn
    def delete_transaction(self, transaction_id):
        """Remove a transaction by id. Returns True if something was deleted."""
        before = len(self.transactions)
        self.transactions = [t for t in self.transactions if t.id != transaction_id]
        deleted = len(self.transactions) != before
        if deleted:
            self._persist()
        return deleted
    def get_transactions(self, month=None, transaction_type=None):
        """Return transactions filtered by 'YYYY-MM' month and/or type."""
        result = self.transactions
        if month:
            result = [t for t in result if t.date.startswith(month)]
        if transaction_type:
            result = [t for t in result if t.type == transaction_type]
        return sorted(result, key=lambda t: t.date, reverse=True)
    # ------------------------------------------------------------------
    # Budgets
    # ------------------------------------------------------------------
    def set_budget(self, category, monthly_limit):
        """Create or update the monthly budget for a category."""
        for budget in self.budgets:
            if budget.category == category:
                budget.monthly_limit = float(monthly_limit)
                self._persist()
                return budget
        budget = Budget(category, monthly_limit)
        self.budgets.append(budget)
        self._persist()
        return budget
    def remove_budget(self, category):
        """Delete the budget for a category. Returns True if removed."""
        before = len(self.budgets)
        self.budgets = [b for b in self.budgets if b.category != category]
        removed = len(self.budgets) != before
        if removed:
            self._persist()
        return removed
    # ------------------------------------------------------------------
    # Savings goals
    # ------------------------------------------------------------------
    def create_savings_goal(self, name, target_amount, deadline=None):
        """Create a new savings goal."""
        goal = SavingsGoal(name, target_amount, deadline)
        self.savings_goals.append(goal)
        self._persist()
        return goal
    def contribute_to_goal(self, goal_id, amount):
        """Add money to a savings goal. Returns the updated goal or None."""
        for goal in self.savings_goals:
            if goal.id == goal_id:
                goal.saved_amount += float(amount)
                self._persist()
                return goal
        return None
    def remove_savings_goal(self, goal_id):
        """Delete a savings goal by id. Returns True if removed."""
        before = len(self.savings_goals)
        self.savings_goals = [g for g in self.savings_goals if g.id != goal_id]
        removed = len(self.savings_goals) != before
        if removed:
            self._persist()
        return removed
    # ------------------------------------------------------------------
    # Calculations / summaries
    # ------------------------------------------------------------------
    def get_category_totals(self, month=None, transaction_type="expense"):
        """Return {category: total_amount} for the given month (default: all time)."""
        totals = defaultdict(float)
        for txn in self.get_transactions(month=month, transaction_type=transaction_type):
            totals[txn.category] += txn.amount
        return dict(totals)
    def get_monthly_summary(self, month=None):
        """Return income, expenses, and net savings for a month (default: current)."""
        if month is None:
            month = datetime.now().strftime("%Y-%m")
        income = sum(t.amount for t in self.get_transactions(month, "income"))
        expenses = sum(t.amount for t in self.get_transactions(month, "expense"))
        return {
            "month": month,
            "income": income,
            "expenses": expenses,
            "net": income - expenses,
        }
    def get_budget_status(self, month=None):
        """Return a list of dicts describing budget vs. actual per category."""
        if month is None:
            month = datetime.now().strftime("%Y-%m")
        spent = self.get_category_totals(month, "expense")
        status = []
        for budget in self.budgets:
            spent_amount = spent.get(budget.category, 0.0)
            remaining = budget.monthly_limit - spent_amount
            pct = (spent_amount / budget.monthly_limit * 100) if budget.monthly_limit > 0 else 0.0
            status.append({
                "category": budget.category,
                "limit": budget.monthly_limit,
                "spent": spent_amount,
                "remaining": remaining,
                "percent_used": min(pct, 999.0),
                "over_budget": spent_amount > budget.monthly_limit,
            })
        return status
    def get_monthly_trends(self, num_months=6):
        """Return per-month income/expense/net for the last N months, oldest first."""
        now = datetime.now()
        months = []
        year, mon = now.year, now.month
        for _ in range(num_months):
            months.append(f"{year:04d}-{mon:02d}")
            mon -= 1
            if mon == 0:
                mon = 12
                year -= 1
        months.reverse()
        trends = []
        for m in months:
            summary = self.get_monthly_summary(m)
            trends.append(summary)
        return trends
    def get_savings_over_time(self, num_months=6):
        """Return cumulative saved amount (income - expenses) at each month end."""
        trends = self.get_monthly_trends(num_months)
        cumulative = 0.0
        points = []
        for entry in trends:
            cumulative += entry["net"]
            points.append({"month": entry["month"], "saved": cumulative})
        return points
    def get_dashboard_stats(self):
        """Return headline numbers for the dashboard view."""
        month = datetime.now().strftime("%Y-%m")
        summary = self.get_monthly_summary(month)
        total_saved_goals = sum(g.saved_amount for g in self.savings_goals)
        total_targets = sum(g.target_amount for g in self.savings_goals)
        return {
            "summary": summary,
            "transaction_count": len(self.transactions),
            "savings_saved": total_saved_goals,
            "savings_target": total_targets,
            "over_budget_categories": [
                s["category"] for s in self.get_budget_status(month) if s["over_budget"]
            ],
        }