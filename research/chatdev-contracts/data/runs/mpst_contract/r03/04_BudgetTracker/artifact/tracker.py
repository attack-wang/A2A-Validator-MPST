import uuid
from datetime import datetime
from models import Transaction, SavingsGoal


class BudgetTracker:
    def __init__(self):
        self.transactions = []
        self.goals = []

    def add_transaction(self, kind, category, description, amount, date=None):
        date = date or datetime.now().strftime("%Y-%m-%d")
        t = Transaction(id=uuid.uuid4().hex[:8], date=date, kind=kind,
                        category=category, description=description, amount=abs(amount))
        self.transactions.append(t)
        return t

    def total_income(self):
        return sum(t.amount for t in self.transactions if t.kind == "income")

    def total_expenses(self):
        return sum(t.amount for t in self.transactions if t.kind == "expense")

    def balance(self):
        return self.total_income() - self.total_expenses()

    def monthly_summary(self, year, month):
        prefix = f"{year:04d}-{month:02d}"
        rows = [t for t in self.transactions if t.date.startswith(prefix)]
        inc = sum(t.amount for t in rows if t.kind == "income")
        exp = sum(t.amount for t in rows if t.kind == "expense")
        return rows, inc, exp, inc - exp

    def category_breakdown(self):
        cats = {}
        for t in self.transactions:
            if t.kind == "expense":
                cats[t.category] = cats.get(t.category, 0.0) + t.amount
        return dict(sorted(cats.items(), key=lambda kv: kv[1], reverse=True))

    def add_goal(self, name, target):
        g = SavingsGoal(name=name, target=abs(target))
        self.goals.append(g)
        return g

    def contribute(self, name, amount):
        for g in self.goals:
            if g.name.lower() == name.lower():
                g.saved = min(g.target, g.saved + abs(amount))
                return g
        return None

    def to_dict(self):
        return {"transactions": [vars(t) for t in self.transactions],
                "goals": [vars(g) for g in self.goals]}

    @classmethod
    def from_dict(cls, data):
        obj = cls()
        obj.transactions = [Transaction(**d) for d in data.get("transactions", [])]
        obj.goals = [SavingsGoal(**d) for d in data.get("goals", [])]
        return obj