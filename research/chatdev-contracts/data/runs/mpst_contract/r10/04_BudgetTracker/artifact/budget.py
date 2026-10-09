"""Core budget tracking logic: transactions, savings goals, and persistence."""
import json
import os
import uuid
from datetime import datetime

DATA_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "budget_data.json")


class Transaction:
    def __init__(self, ttype, category, amount, note="", date=None, tid=None):
        self.id = tid or uuid.uuid4().hex[:8]
        self.type = ttype  # "income" or "expense"
        self.category = category
        self.amount = round(float(amount), 2)
        self.note = note
        self.date = date or datetime.now().strftime("%Y-%m-%d")

    def to_dict(self):
        return {"id": self.id, "type": self.type, "category": self.category,
                "amount": self.amount, "note": self.note, "date": self.date}

    @classmethod
    def from_dict(cls, d):
        return cls(d["type"], d["category"], d["amount"], d.get("note", ""),
                   d.get("date"), d.get("id"))


class SavingsGoal:
    def __init__(self, name, target, saved=0.0):
        self.name = name
        self.target = round(float(target), 2)
        self.saved = round(float(saved), 2)

    def to_dict(self):
        return {"name": self.name, "target": self.target, "saved": self.saved}

    @classmethod
    def from_dict(cls, d):
        return cls(d["name"], d["target"], d.get("saved", 0.0))

    @property
    def progress(self):
        if self.target <= 0:
            return 100.0
        return min(100.0, round(self.saved / self.target * 100, 1))


class BudgetManager:
    def __init__(self, path=DATA_FILE):
        self.path = path
        self.transactions = []
        self.goals = []
        self.load()

    def load(self):
        if os.path.exists(self.path):
            try:
                with open(self.path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                self.transactions = [Transaction.from_dict(d) for d in data.get("transactions", [])]
                self.goals = [SavingsGoal.from_dict(d) for d in data.get("goals", [])]
            except (json.JSONDecodeError, KeyError, TypeError):
                self.transactions, self.goals = [], []

    def save(self):
        data = {"transactions": [t.to_dict() for t in self.transactions],
                "goals": [g.to_dict() for g in self.goals]}
        with open(self.path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)

    def add_transaction(self, ttype, category, amount, note=""):
        if ttype not in ("income", "expense"):
            raise ValueError("Type must be 'income' or 'expense'.")
        if amount <= 0:
            raise ValueError("Amount must be positive.")
        t = Transaction(ttype, category, amount, note)
        self.transactions.append(t)
        self.save()
        return t

    def delete_transaction(self, tid):
        for t in self.transactions:
            if t.id == tid:
                self.transactions.remove(t)
                self.save()
                return True
        return False

    def add_goal(self, name, target):
        if target <= 0:
            raise ValueError("Target must be positive.")
        if any(g.name.lower() == name.lower() for g in self.goals):
            raise ValueError("Goal already exists.")
        g = SavingsGoal(name, target)
        self.goals.append(g)
        self.save()
        return g

    def contribute(self, name, amount):
        if amount <= 0:
            raise ValueError("Amount must be positive.")
        for g in self.goals:
            if g.name.lower() == name.lower():
                g.saved = round(min(g.target, g.saved + amount), 2)
                self.save()
                return g
        raise ValueError("Goal not found.")

    def totals(self):
        income = sum(t.amount for t in self.transactions if t.type == "income")
        expenses = sum(t.amount for t in self.transactions if t.type == "expense")
        return round(income, 2), round(expenses, 2), round(income - expenses, 2)

    def by_category(self):
        cats = {}
        for t in self.transactions:
            if t.type == "expense":
                cats[t.category] = round(cats.get(t.category, 0.0) + t.amount, 2)
        return cats

    def summary(self):
        income, expenses, balance = self.totals()
        lines = ["=== Budget Summary ===",
                 f"Total income:   ${income:,.2f}",
                 f"Total expenses: ${expenses:,.2f}",
                 f"Net balance:    ${balance:,.2f}", ""]
        cats = self.by_category()
        lines.append("Expenses by category:")
        if cats:
            for c, amt in sorted(cats.items(), key=lambda x: -x[1]):
                pct = (amt / expenses * 100) if expenses else 0
                lines.append(f"  {c:<15} ${amt:,.2f} ({pct:.1f}%)")
        else:
            lines.append("  (none)")
        lines.append("")
        lines.append("Savings goals:")
        if self.goals:
            for g in self.goals:
                bar_len = 20
                filled = int(bar_len * g.progress / 100)
                bar = "#" * filled + "-" * (bar_len - filled)
                lines.append(f"  {g.name:<15} ${g.saved:,.2f} / ${g.target:,.2f} [{bar}] {g.progress:.1f}%")
        else:
            lines.append("  (none)")
        return "\n".join(lines)

    def list_transactions(self):
        if not self.transactions:
            return "No transactions recorded."
        lines = [f"{'ID':<10}{'Date':<12}{'Type':<9}{'Category':<15}{'Amount':>12}  Note"]
        for t in sorted(self.transactions, key=lambda x: x.date, reverse=True):
            sign = "+" if t.type == "income" else "-"
            lines.append(f"{t.id:<10}{t.date:<12}{t.type:<9}{t.category:<15}{sign}${t.amount:>10,.2f}  {t.note}")
        return "\n".join(lines)