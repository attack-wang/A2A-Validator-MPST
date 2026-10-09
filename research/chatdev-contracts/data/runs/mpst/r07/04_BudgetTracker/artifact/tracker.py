"""
tracker.py
Core business logic for the Budget Tracker application.
...
"""
from datetime import date, datetime, timedelta
from typing import Dict, List, Optional, Union
from models import Expense, SavingsGoal
from storage import Storage
DateLike = Union[str, date]
class BudgetTracker:
    """Manages expenses, savings goals, and budget settings."""
    DEFAULT_CATEGORIES = [
        "Food", "Housing", "Transport", "Utilities",
        "Entertainment", "Health", "Shopping", "Other",
    ]
    def __init__(self, storage: Optional[Storage] = None):
        self.storage = storage or Storage()
        self.expenses: List[Expense] = []
        self.savings_goals: List[SavingsGoal] = []
        self.monthly_budget: float = 0.0
        self._load()
    # -- persistence ---------------------------------------------------
    def _load(self) -> None:
        data = self.storage.load()
        self.expenses = [Expense.from_dict(d) for d in data.get("expenses", [])]
        self.savings_goals = [SavingsGoal.from_dict(d) for d in data.get("savings_goals", [])]
        self.monthly_budget = float(data.get("settings", {}).get("monthly_budget", 0.0))
    def _save(self) -> None:
        self.storage.save({
            "expenses": [e.to_dict() for e in self.expenses],
            "savings_goals": [g.to_dict() for g in self.savings_goals],
            "settings": {"monthly_budget": self.monthly_budget},
        })
    # -- date helpers ----------------------------------------------------
    @staticmethod
    def _to_date(value: DateLike) -> date:
        if isinstance(value, date):
            return value
        return datetime.strptime(str(value), "%Y-%m-%d").date()
    @staticmethod
    def _end_of_month(year: int, month: int) -> date:
        if month == 12:
            return date(year, 12, 31)
        return date(year, month + 1, 1) - timedelta(days=1)
    # -- expense management ---------------------------------------------
    def add_expense(self, amount, category, description="", expense_date=None) -> Expense:
        amount = float(amount)
        if amount <= 0:
            raise ValueError("Expense amount must be positive.")
        if not category:
            raise ValueError("Expense category cannot be empty.")
        date_str = self._to_date(expense_date).isoformat() if expense_date is not None else date.today().isoformat()
        expense = Expense(amount=amount, category=category, description=description, date_str=date_str)
        self.expenses.append(expense)
        self._save()
        return expense
    def update_expense(self, expense_id, amount=None, category=None, description=None, expense_date=None) -> bool:
        expense = self.find_expense(expense_id)
        if expense is None:
            return False
        if amount is not None:
            amount = float(amount)
            if amount <= 0:
                raise ValueError("Expense amount must be positive.")
            expense.amount = round(amount, 2)
        if category is not None:
            if not category:
                raise ValueError("Expense category cannot be empty.")
            expense.category = category
        if description is not None:
            expense.description = description
        if expense_date is not None:
            expense.date_str = self._to_date(expense_date).isoformat()
        self._save()
        return True
    def delete_expense(self, expense_id) -> bool:
        expense = self.find_expense(expense_id)
        if expense is None:
            return False
        self.expenses.remove(expense)
        self._save()
        return True
    def find_expense(self, expense_id) -> Optional[Expense]:
        for e in self.expenses:
            if e.expense_id == expense_id:
                return e
        return None
    # -- reporting --------------------------------------------------------
    def get_expenses_by_category(self, start_date=None, end_date=None) -> Dict[str, float]:
        start = self._to_date(start_date) if start_date is not None else None
        end = self._to_date(end_date) if end_date is not None else None
        totals: Dict[str, float] = {}
        for e in self.expenses:
            d = e.date
            if start is not None and d < start:
                continue
            if end is not None and d > end:
                continue
            totals[e.category] = round(totals.get(e.category, 0.0) + e.amount, 2)
        return totals
    def get_monthly_trend(self, year: int) -> Dict[int, float]:
        trend = {m: 0.0 for m in range(1, 13)}
        for e in self.expenses:
            d = e.date
            if d.year == year:
                trend[d.month] = round(trend[d.month] + e.amount, 2)
        return trend
    def get_month_spent(self, year=None, month=None) -> float:
        today = date.today()
        year = int(year) if year is not None else today.year
        month = int(month) if month is not None else today.month
        start = date(year, month, 1)
        end = self._end_of_month(year, month)
        return round(sum(e.amount for e in self.expenses if start <= e.date <= end), 2)
    def get_dashboard_summary(self) -> Dict[str, float]:
        spent = self.get_month_spent()
        budget = self.monthly_budget
        total_saved = round(sum(g.saved_amount for g in self.savings_goals), 2)
        return {
            "month_spent": spent,
            "monthly_budget": budget,
            "budget_remaining": round(budget - spent, 2) if budget > 0 else 0.0,
            "over_budget": spent > budget if budget > 0 else False,
            "total_saved": total_saved,
            "goals_count": len(self.savings_goals),
            "goals_completed": sum(1 for g in self.savings_goals if g.is_complete),
        }
    # -- savings goals ------------------------------------------------------
    def add_goal(self, name, target_amount, deadline_str="") -> SavingsGoal:
        name = str(name).strip()
        if not name:
            raise ValueError("Goal name cannot be empty.")
        target_amount = float(target_amount)
        if target_amount <= 0:
            raise ValueError("Goal target amount must be positive.")
        if deadline_str:
            datetime.strptime(deadline_str, "%Y-%m-%d")  # validate format
        goal = SavingsGoal(name=name, target_amount=target_amount, deadline_str=deadline_str)
        self.savings_goals.append(goal)
        self._save()
        return goal
    def contribute_to_goal(self, goal_id, amount) -> float:
        goal = self.find_goal(goal_id)
        if goal is None:
            raise KeyError(f"No savings goal with id '{goal_id}'.")
        amount = float(amount)
        if amount <= 0:
            raise ValueError("Contribution must be positive.")
        goal.contribute(amount)
        self._save()
        return goal.saved_amount
    def withdraw_from_goal(self, goal_id, amount) -> float:
        goal = self.find_goal(goal_id)
        if goal is None:
            raise KeyError(f"No savings goal with id '{goal_id}'.")
        amount = float(amount)
        if amount <= 0:
            raise ValueError("Withdrawal must be positive.")
        if amount > goal.saved_amount:
            raise ValueError("Withdrawal exceeds the amount saved in this goal.")
        goal.saved_amount = round(goal.saved_amount - amount, 2)
        self._save()
        return goal.saved_amount
    def delete_goal(self, goal_id) -> bool:
        goal = self.find_goal(goal_id)
        if goal is None:
            return False
        self.savings_goals.remove(goal)
        self._save()
        return True
    def find_goal(self, goal_id) -> Optional[SavingsGoal]:
        for g in self.savings_goals:
            if g.goal_id == goal_id:
                return g
        return None
    # -- settings ---------------------------------------------------------
    def set_monthly_budget(self, amount) -> None:
        amount = float(amount)
        if amount < 0:
            raise ValueError("Monthly budget cannot be negative.")
        self.monthly_budget = round(amount, 2)
        self._save()