import datetime
from collections import defaultdict

import storage
from models import SavingsGoal, Transaction


class BudgetTracker:
    def __init__(self):
        self.data = storage.load()

    def _save(self):
        storage.save(self.data)

    def add_transaction(self, ttype, amount, category, description, date=None):
        if ttype not in ("expense", "income"):
            raise ValueError("Type must be 'expense' or 'income'.")
        amount = float(amount)
        if amount <= 0:
            raise ValueError("Amount must be positive.")
        date = date or datetime.date.today().isoformat()
        datetime.date.fromisoformat(date)
        txn = Transaction(self.data["next_id"], date, ttype,
                          category or "Uncategorized", description or "", amount)
        self.data["next_id"] += 1
        self.data["transactions"].append(txn.to_dict())
        self._save()
        return txn

    def delete_transaction(self, txn_id):
        before = len(self.data["transactions"])
        self.data["transactions"] = [t for t in self.data["transactions"]
                                     if t["id"] != txn_id]
        removed = len(self.data["transactions"]) < before
        if removed:
            self._save()
        return removed

    def transactions(self, month=None):
        txns = [Transaction.from_dict(t) for t in self.data["transactions"]]
        if month:
            txns = [t for t in txns if t.date.startswith(month)]
        return sorted(txns, key=lambda t: (t.date, t.id))

    def summary(self, month=None):
        txns = self.transactions(month)
        income = sum(t.amount for t in txns if t.ttype == "income")
        expenses = sum(t.amount for t in txns if t.ttype == "expense")
        return income, expenses, income - expenses

    def category_breakdown(self, month=None):
        totals = defaultdict(float)
        for t in self.transactions(month):
            if t.ttype == "expense":
                totals[t.category] += t.amount
        return dict(sorted(totals.items(), key=lambda kv: kv[1], reverse=True))

    def add_goal(self, name, target):
        name = (name or "").strip()
        if not name:
            raise ValueError("Goal name is required.")
        target = float(target)
        if target <= 0:
            raise ValueError("Target must be positive.")
        if any(g["name"].lower() == name.lower() for g in self.data["goals"]):
            raise ValueError("A goal with that name already exists.")
        goal = SavingsGoal(name, target)
        self.data["goals"].append(goal.to_dict())
        self._save()
        return goal

    def contribute(self, name, amount):
        amount = float(amount)
        if amount <= 0:
            raise ValueError("Amount must be positive.")
        for g in self.data["goals"]:
            if g["name"].lower() == (name or "").strip().lower():
                g["saved"] = round(min(g["saved"] + amount, g["target"]), 2)
                self._save()
                return SavingsGoal.from_dict(g)
        raise ValueError("Goal not found.")

    def goals(self):
        return [SavingsGoal.from_dict(g) for g in self.data["goals"]]

    def total_saved(self):
        return sum(g["saved"] for g in self.data["goals"])