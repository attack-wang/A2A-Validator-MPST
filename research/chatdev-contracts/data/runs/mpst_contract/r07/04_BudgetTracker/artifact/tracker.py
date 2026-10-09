import storage
from models import Transaction


class BudgetTracker:
    def __init__(self):
        self.data = storage.load()

    def add(self, kind, category, amount, note=""):
        t = Transaction(kind, category, round(amount, 2), note)
        self.data["transactions"].append(t.to_dict())
        storage.save(self.data)
        return t

    def remove(self, index):
        txns = self.data["transactions"]
        if 0 <= index < len(txns):
            removed = txns.pop(index)
            storage.save(self.data)
            return removed
        return None

    def set_goal(self, amount):
        self.data["savings_goal"] = round(amount, 2)
        storage.save(self.data)

    def totals(self):
        income = sum(t["amount"] for t in self.data["transactions"]
                     if t["kind"] == "income")
        expenses = sum(t["amount"] for t in self.data["transactions"]
                       if t["kind"] == "expense")
        return income, expenses, income - expenses

    def by_category(self):
        cats = {}
        for t in self.data["transactions"]:
            if t["kind"] == "expense":
                cats[t["category"]] = cats.get(t["category"], 0.0) + t["amount"]
        return cats

    def savings_progress(self):
        _, _, balance = self.totals()
        goal = self.data.get("savings_goal", 0.0)
        pct = (balance / goal * 100) if goal > 0 else 0.0
        return balance, goal, min(pct, 100.0)

    def list_transactions(self):
        return self.data["transactions"]