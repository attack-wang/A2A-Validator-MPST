'''
tracker.py
Core business logic for the budget tracker.
'''
from collections import defaultdict
from models import Expense, SavingsGoal
class BudgetTracker:
    """Manages expenses and savings goals, backed by a storage layer."""
    def __init__(self, storage):
        self.storage = storage
        data = storage.load()
        self.expenses = [Expense.from_dict(e) for e in data["expenses"]]
        self.savings_goals = [SavingsGoal.from_dict(g) for g in data["savings_goals"]]
    def save(self):
        data = {
            "expenses": [e.to_dict() for e in self.expenses],
            "savings_goals": [g.to_dict() for g in self.savings_goals],
        }
        self.storage.save(data)
    # ---- Expenses ----
    def add_expense(self, amount, category, description="", date=None):
        expense = Expense(amount, category, description, date)
        self.expenses.append(expense)
        self.save()
        return expense
    def remove_expense(self, expense_id):
        """Remove the expense with the given id; returns True if removed."""
        for i, expense in enumerate(self.expenses):
            if expense.id == expense_id:
                del self.expenses[i]
                self.save()
                return True
        return False
    def get_expense(self, expense_id):
        for expense in self.expenses:
            if expense.id == expense_id:
                return expense
        return None
    def get_expenses_sorted(self):
        return sorted(self.expenses, key=lambda e: e.date, reverse=True)
    def total_expenses(self):
        return sum(e.amount for e in self.expenses)
    def expenses_by_category(self):
        totals = defaultdict(float)
        for e in self.expenses:
            totals[e.category] += e.amount
        return dict(totals)
    def monthly_expenses(self):
        totals = defaultdict(float)
        for e in self.expenses:
            month = e.date[:7]
            totals[month] += e.amount
        return dict(sorted(totals.items()))
    def expenses_in_month(self, year_month):
        return [e for e in self.expenses if e.date.startswith(year_month)]
    # ---- Savings ----
    def add_goal(self, name, target_amount):
        goal = SavingsGoal(name, target_amount)
        self.savings_goals.append(goal)
        self.save()
        return goal
    def get_goal(self, goal_id):
        for goal in self.savings_goals:
            if goal.id == goal_id:
                return goal
        return None
    def remove_goal(self, goal_id):
        for i, goal in enumerate(self.savings_goals):
            if goal.id == goal_id:
                del self.savings_goals[i]
                self.save()
                return True
        return False
    def deposit(self, goal_id, amount):
        goal = self.get_goal(goal_id)
        if goal is None:
            raise ValueError(f"No savings goal with id {goal_id}.")
        goal.deposit(amount)
        self.save()
        return goal
    def withdraw(self, goal_id, amount):
        goal = self.get_goal(goal_id)
        if goal is None:
            raise ValueError(f"No savings goal with id {goal_id}.")
        goal.withdraw(amount)
        self.save()
        return goal
    def total_saved(self):
        return sum(g.saved_amount for g in self.savings_goals)
    # ---- Summary ----
    def summary(self):
        """Return a multi-line text summary of expenses and savings."""
        lines = ["=== Budget Summary ==="]
        lines.append(f"Total expenses: {self.total_expenses():.2f}")
        lines.append(f"Total saved:    {self.total_saved():.2f}")
        lines.append("")
        lines.append("Expenses by category:")
        by_cat = self.expenses_by_category()
        if by_cat:
            for cat, val in sorted(by_cat.items(), key=lambda kv: kv[1], reverse=True):
                lines.append(f"  {cat:<15} {val:>10.2f}")
        else:
            lines.append("  (no expenses recorded)")
        lines.append("")
        lines.append("Savings goals:")
        if self.savings_goals:
            for g in self.savings_goals:
                status = "COMPLETE" if g.is_complete else f"{g.progress:.1f}%"
                lines.append(
                    f"  {g.name:<15} {g.saved_amount:>10.2f} / {g.target_amount:>10.2f} ({status})"
                )
        else:
            lines.append("  (no goals set)")
        return "\n".join(lines)