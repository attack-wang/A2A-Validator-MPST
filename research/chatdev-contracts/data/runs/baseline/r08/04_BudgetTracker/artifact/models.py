'''
models.py
Data models for the Budget Tracker application.
Contains:
    - Transaction: a single expense or income record.
    - SavingsGoal: a named savings target with progress tracking.
    - Budget: aggregate manager for transactions and goals, providing
      the statistics consumed by the GUI and charts.
'''
import uuid
from datetime import datetime
class Transaction:
    """A single financial transaction (expense or income)."""
    EXPENSE = "expense"
    INCOME = "income"
    def __init__(self, amount, category, description="", date=None,
                 t_type=EXPENSE, trans_id=None):
        self.id = trans_id if trans_id is not None else str(uuid.uuid4())
        self.amount = round(float(amount), 2)
        self.category = category
        self.description = description
        self.date = date or datetime.now().strftime("%Y-%m-%d")
        self.type = t_type
    def to_dict(self):
        return {...}
    @classmethod
    def from_dict(cls, data):
        ...
class SavingsGoal:
    """A named savings target with progress tracking."""
    def __init__(self, name, target_amount, current_amount=0.0,
                 deadline=None, goal_id=None):
        self.id = goal_id if goal_id is not None else str(uuid.uuid4())
        self.name = name
        self.target_amount = round(float(target_amount), 2)
        self.current_amount = round(float(current_amount), 2)
        self.deadline = deadline
    def add_contribution(self, amount):
        self.current_amount = round(self.current_amount + float(amount), 2)
    def progress(self):
        if self.target_amount <= 0:
            return 0.0
        return min(100.0, (self.current_amount / self.target_amount) * 100.0)
    def is_complete(self):
        return self.current_amount >= self.target_amount
    def to_dict(self):
        return {"id": self.id, "name": self.name, "target_amount": self.target_amount,
                "current_amount": self.current_amount, "deadline": self.deadline}
    @classmethod
    def from_dict(cls, data):
        return cls(name=data.get("name", "Goal"),
                   target_amount=data.get("target_amount", 0.0),
                   current_amount=data.get("current_amount", 0.0),
                   deadline=data.get("deadline"),
                   goal_id=data.get("id"))
class Budget:
    """Manages all transactions and savings goals; computes statistics."""
    def __init__(self, transactions=None, goals=None):
        self.transactions = list(transactions or [])
        self.goals = list(goals or [])
    # --- transactions ---
    def add_transaction(self, txn):
        self.transactions.append(txn)
    def get_transaction(self, txn_id):
        for t in self.transactions:
            if t.id == txn_id:
                return t
        return None
    def update_transaction(self, txn_id, **fields):
        txn = self.get_transaction(txn_id)
        if txn is None:
            return False
        for key, value in fields.items():
            if hasattr(txn, key):
                setattr(txn, key, value)
        txn.amount = round(float(txn.amount), 2)
        return True
    def delete_transaction(self, txn_id):
        txn = self.get_transaction(txn_id)
        if txn is not None:
            self.transactions.remove(txn)
    # --- goals ---
    def add_goal(self, goal):
        self.goals.append(goal)
    def get_goal(self, goal_id):
        for g in self.goals:
            if g.id == goal_id:
                return g
        return None
    def update_goal(self, goal_id, **fields):
        goal = self.get_goal(goal_id)
        if goal is None:
            return False
        for key, value in fields.items():
            if hasattr(goal, key):
                setattr(goal, key, value)
        goal.target_amount = round(float(goal.target_amount), 2)
        goal.current_amount = round(float(goal.current_amount), 2)
        return True
    def delete_goal(self, goal_id):
        goal = self.get_goal(goal_id)
        if goal is not None:
            self.goals.remove(goal)
    def contribute_to_goal(self, goal_id, amount):
        goal = self.get_goal(goal_id)
        if goal is not None:
            goal.add_contribution(amount)
    # --- statistics ---
    def total_income(self):
        return round(sum(t.amount for t in self.transactions if t.type == Transaction.INCOME), 2)
    def total_expenses(self):
        return round(sum(t.amount for t in self.transactions if t.type == Transaction.EXPENSE), 2)
    def net_savings(self):
        return round(self.total_income() - self.total_expenses(), 2)
    def category_totals(self):
        totals = {}
        for t in self.transactions:
            if t.type == Transaction.EXPENSE:
                totals[t.category] = totals.get(t.category, 0.0) + t.amount
        return dict(sorted(totals.items(), key=lambda kv: kv[1], reverse=True))
    def monthly_summary(self):
        summary = {}
        for t in self.transactions:
            month = t.date[:7]
            bucket = summary.setdefault(month, {"income": 0.0, "expense": 0.0})
            bucket[t.type] += t.amount
        return dict(sorted(summary.items()))
    def monthly_savings_series(self):
        return [(m, round(d["income"] - d["expense"], 2)) for m, d in self.monthly_summary().items()]
    def monthly_comparison_series(self):
        return [(m, round(d["income"], 2), round(d["expense"], 2)) for m, d in self.monthly_summary().items()]
    def transactions_sorted(self):
        return sorted(self.transactions, key=lambda t: (t.date, t.type), reverse=False)