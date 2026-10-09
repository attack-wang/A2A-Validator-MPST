'''
tracker.py
Business logic layer for the Budget Tracker.
BudgetTracker owns all in-memory state (transactions, savings goals,
category budgets) and delegates persistence to a storage object.
It provides CRUD operations plus analytics methods that feed the
reporting layer (reports.py) and the CLI (cli.py).
'''
import csv
from datetime import date, timedelta
from models import Transaction, SavingsGoal, CategoryBudget
class BudgetTracker:
    def __init__(self, storage):
        self.storage = storage
        self.transactions = []
        self.goals = []
        self.category_budgets = {}
        self.load()
    def load(self):
        state = self.storage.load()
        self.transactions = [Transaction.from_dict(d) for d in state["transactions"]]
        self.goals = [SavingsGoal.from_dict(d) for d in state["goals"]]
        self.category_budgets = {}
        for d in state["category_budgets"]:
            budget = CategoryBudget.from_dict(d)
            self.category_budgets[budget.name] = budget
    def save(self):
        state = {
            "transactions": [t.to_dict() for t in self.transactions],
            "goals": [g.to_dict() for g in self.goals],
            "category_budgets": [b.to_dict() for b in self.category_budgets.values()],
        }
        self.storage.save(state)
    # --- transactions ---
    def add_transaction(self, amount, category, t_type, description="", date_str=None):
        tx = Transaction(amount, category, t_type, description, date_str or date.today().isoformat())
        self.transactions.append(tx)
        self.save()
        return tx
    def get_transaction(self, tx_id):
        return next((t for t in self.transactions if t.id == tx_id), None)
    def update_transaction(self, tx_id, amount=None, category=None, t_type=None, description=None, date_str=None):
        tx = self.get_transaction(tx_id)
        if tx is None:
            return False
        try:
            updated = Transaction(
                amount if amount is not None else tx.amount,
                category if category is not None else tx.category,
                t_type if t_type is not None else tx.t_type,
                description if description is not None else tx.description,
                date_str if date_str is not None else tx.date,
                tx.id,
            )
        except ValueError:
            return False
        self.transactions[self.transactions.index(tx)] = updated
        self.save()
        return True
    def delete_transaction(self, tx_id):
        tx = self.get_transaction(tx_id)
        if tx is None:
            return False
        self.transactions.remove(tx)
        self.save()
        return True
    def transactions_sorted(self, reverse=True):
        return sorted(self.transactions, key=lambda t: (t.date, t.id), reverse=reverse)
    # --- goals ---
    def add_goal(self, name, target_amount, deadline=None):
        goal = SavingsGoal(name, target_amount, deadline)
        self.goals.append(goal)
        self.save()
        return goal
    def get_goal(self, goal_id):
        return next((g for g in self.goals if g.id == goal_id), None)
    def delete_goal(self, goal_id):
        goal = self.get_goal(goal_id)
        if goal is None:
            return False
        self.goals.remove(goal)
        self.save()
        return True
    # --- budgets ---
    def set_budget(self, name, monthly_limit):
        budget = CategoryBudget(name, monthly_limit)
        self.category_budgets[budget.name] = budget
        self.save()
        return budget
    def remove_budget(self, name):
        if name in self.category_budgets:
            del self.category_budgets[name]
            self.save()
            return True
        return False
    # --- analytics ---
    def totals(self):
        income = sum(t.amount for t in self.transactions if t.t_type == "income")
        expenses = sum(t.amount for t in self.transactions if t.t_type == "expense")
        savings = sum(t.amount for t in self.transactions if t.t_type == "savings")
        return {
            "income": round(income, 2),
            "expenses": round(expenses, 2),
            "savings": round(savings, 2),
            "balance": round(income - expenses - savings, 2),
        }
    def monthly_summary(self):
        summary = {}
        for t in self.transactions:
            month = t.date[:7]  # YYYY-MM
            data = summary.setdefault(month, {"income": 0.0, "expense": 0.0, "savings": 0.0, "net": 0.0})
            if t.t_type == "income":
                data["income"] += t.amount
            elif t.t_type == "expense":
                data["expense"] += t.amount
            else:
                data["savings"] += t.amount
            data["net"] = data["income"] - data["expense"] - data["savings"]
        for data in summary.values():
            for key in ("income", "expense", "savings", "net"):
                data[key] = round(data[key], 2)
        return dict(sorted(summary.items()))
    def spending_by_category(self):
        spending = {}
        for t in self.transactions:
            if t.t_type == "expense":
                spending[t.category] = spending.get(t.category, 0.0) + t.amount
        return {cat: round(amount, 2) for cat, amount in spending.items()}
    def budget_status(self):
        if not self.category_budgets:
            return []
        current_month = date.today().strftime("%Y-%m")
        spent_by_category = {}
        for t in self.transactions:
            if t.t_type == "expense" and t.date[:7] == current_month:
                spent_by_category[t.category] = spent_by_category.get(t.category, 0.0) + t.amount
        status = []
        for name in sorted(self.category_budgets):
            budget = self.category_budgets[name]
            spent = round(spent_by_category.get(name, 0.0), 2)
            percent = (spent / budget.monthly_limit * 100) if budget.monthly_limit else 0.0
            status.append({
                "category": name,
                "spent": spent,
                "limit": budget.monthly_limit,
                "percent": round(percent, 1),
                "over": spent > budget.monthly_limit,
            })
        return status
    def savings_progress(self):
        saved_total = sum(t.amount for t in self.transactions if t.t_type == "savings")
        progress = []
        for goal in self.goals:
            percent = (saved_total / goal.target_amount * 100) if goal.target_amount else 0.0
            progress.append({
                "id": goal.id,
                "name": goal.name,
                "target": goal.target_amount,
                "saved": round(min(saved_total, goal.target_amount), 2),
                "percent": round(percent, 1),
                "deadline": goal.deadline,
                "complete": saved_total >= goal.target_amount,
            })
        return progress