'''
tracker.py
Core business logic for the Budget Tracker application.
Provides the BudgetTracker class, which manages transactions, budgets,
and savings goals, validates user input, computes summaries, and
persists all data through the Storage layer.
'''
from datetime import datetime
from models import (Transaction, Budget, SavingsGoal,
                    TRANSACTION_TYPES, DEFAULT_CATEGORIES)
from storage import Storage
class BudgetTracker:
    """Coordinates transactions, budgets, and savings goals."""
    def __init__(self, storage=None):
        self.storage = storage or Storage()
        self.transactions = []
        self.budgets = []
        self.goals = []
        self.load()
    # -- persistence ----------------------------------------------------
    def save(self):
        """Persist all data through the Storage layer."""
        data = {
            "transactions": [t.to_dict() for t in self.transactions],
            "budgets": [b.to_dict() for b in self.budgets],
            "goals": [g.to_dict() for g in self.goals],
        }
        return self.storage.save(data)
    def load(self):
        """Load previously saved data, if any."""
        data = self.storage.load()
        if not data:
            return
        self.transactions = [Transaction.from_dict(d)
                             for d in data.get("transactions", [])]
        self.budgets = [Budget.from_dict(d)
                        for d in data.get("budgets", [])]
        self.goals = [SavingsGoal.from_dict(d)
                      for d in data.get("goals", [])]
    # -- transactions -----------------------------------------------------
    def add_transaction(self, date, description, amount, category, t_type):
        """Validate and add a new transaction. Returns (ok, message)."""
        if not Transaction.is_valid_date(date):
            return False, "Date must be in YYYY-MM-DD format."
        if not Transaction.is_valid_amount(amount):
            return False, "Amount must be a positive number."
        if t_type not in TRANSACTION_TYPES:
            return False, "Type must be 'expense' or 'income'."
        if not description.strip():
            return False, "Description cannot be empty."
        if not category:
            return False, "Please choose a category."
        amount_value = round(float(amount), 2)
        transaction = Transaction(date=date.strip(),
                                  description=description.strip(),
                                  amount=amount_value,
                                  category=category,
                                  t_type=t_type)
        self.transactions.append(transaction)
        self.save()
        return True, f"{t_type.capitalize()} of {amount_value:.2f} recorded."
    def remove_transaction(self, transaction_id):
        """Delete the transaction with the given id. Returns True on success."""
        for index, transaction in enumerate(self.transactions):
            if transaction.id == transaction_id:
                del self.transactions[index]
                self.save()
                return True
        return False
    def get_categories(self):
        """Return the default spending categories."""
        return list(DEFAULT_CATEGORIES)
    # -- budgets -----------------------------------------------------------
    def set_budget(self, category, monthly_limit):
        """Create or update the monthly limit for a category."""
        try:
            limit_value = round(float(monthly_limit), 2)
        except (TypeError, ValueError):
            return False, "Budget limit must be a number."
        if limit_value < 0:
            return False, "Budget limit cannot be negative."
        for budget in self.budgets:
            if budget.category == category:
                budget.monthly_limit = limit_value
                self.save()
                return True, f"Budget for {category} updated to {limit_value:.2f}."
        self.budgets.append(Budget(category=category,
                                   monthly_limit=limit_value))
        self.save()
        return True, f"Budget for {category} set to {limit_value:.2f}."
    def remove_budget(self, category):
        """Delete the budget for a category. Returns True on success."""
        for index, budget in enumerate(self.budgets):
            if budget.category == category:
                del self.budgets[index]
                self.save()
                return True
        return False
    def budget_status(self, month=None):
        """Return per-category spending vs limit for the given month."""
        month = month or datetime.now().strftime("%Y-%m")
        spent = {}
        for t in self.transactions:
            if t.type == "expense" and t.month == month:
                spent[t.category] = round(spent.get(t.category, 0.0)
                                          + t.amount, 2)
        status = []
        for budget in self.budgets:
            used = spent.get(budget.category, 0.0)
            status.append({
                "category": budget.category,
                "limit": budget.monthly_limit,
                "spent": used,
                "remaining": round(budget.monthly_limit - used, 2),
                "over": used > budget.monthly_limit,
            })
        return status
    # -- savings goals -------------------------------------------------------
    def add_goal(self, name, target_amount, deadline=None):
        """Validate and create a new savings goal. Returns (ok, message)."""
        if not name.strip():
            return False, "Goal name cannot be empty."
        try:
            target = round(float(target_amount), 2)
        except (TypeError, ValueError):
            return False, "Target amount must be a number."
        if target <= 0:
            return False, "Target amount must be positive."
        if deadline and not Transaction.is_valid_date(deadline):
            return False, "Deadline must be in YYYY-MM-DD format."
        goal = SavingsGoal(name=name.strip(), target_amount=target,
                           deadline=deadline or None)
        self.goals.append(goal)
        self.save()
        return True, f"Savings goal '{goal.name}' created."
    def contribute_to_goal(self, goal_id, amount):
        """Add money to a savings goal. Returns (ok, message)."""
        try:
            value = round(float(amount), 2)
        except (TypeError, ValueError):
            return False, "Contribution must be a number."
        if value <= 0:
            return False, "Contribution must be positive."
        for goal in self.goals:
            if goal.id == goal_id:
                goal.contribute(value)
                self.save()
                message = f"Added {value:.2f} to '{goal.name}'."
                if goal.is_complete():
                    message += " Goal complete!"
                return True, message
        return False, "Goal not found."
    def remove_goal(self, goal_id):
        """Delete a savings goal. Returns True on success."""
        for index, goal in enumerate(self.goals):
            if goal.id == goal_id:
                del self.goals[index]
                self.save()
                return True
        return False
    # -- reports ---------------------------------------------------------------
    def monthly_summary(self, month=None):
        """Return (income, expenses, net) totals for the given month key."""
        month = month or datetime.now().strftime("%Y-%m")
        income = sum(t.amount for t in self.transactions
                     if t.type == "income" and t.month == month)
        expenses = sum(t.amount for t in self.transactions
                       if t.type == "expense" and t.month == month)
        return round(income, 2), round(expenses, 2), round(income - expenses, 2)
    def category_totals(self, month=None):
        """Return {category: total_expense} for the given month key."""
        month = month or datetime.now().strftime("%Y-%m")
        totals = {}
        for t in self.transactions:
            if t.type == "expense" and t.month == month:
                totals[t.category] = round(totals.get(t.category, 0.0)
                                           + t.amount, 2)
        return totals
    def recent_months(self, count=6):
        """Return the last `count` month keys ('YYYY-MM'), oldest first."""
        today = datetime.now()
        months = []
        year, month = today.year, today.month
        for _ in range(count):
            months.append(f"{year:04d}-{month:02d}")
            month -= 1
            if month == 0:
                month = 12
                year -= 1
        months.reverse()
        return months
    def savings_by_month(self, count=6):
        """Return ([month keys], [net savings]) for the recent months."""
        months = self.recent_months(count)
        values = []
        for month in months:
            income, expenses, _ = self.monthly_summary(month)
            values.append(round(income - expenses, 2))
        return months, values
    def goal_progress(self):
        """Return [(name, saved, target, percent)] for all goals."""
        return [(g.name, g.saved_amount, g.target_amount,
                 g.progress_percent()) for g in self.goals]