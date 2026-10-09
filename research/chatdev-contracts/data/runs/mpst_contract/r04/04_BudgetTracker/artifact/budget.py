from dataclasses import dataclass, field, asdict
from datetime import datetime
from typing import List
import uuid


@dataclass
class Transaction:
    kind: str  # "expense" or "income"
    category: str
    amount: float
    note: str = ""
    date: str = field(default_factory=lambda: datetime.now().strftime("%Y-%m-%d"))
    tid: str = field(default_factory=lambda: uuid.uuid4().hex[:8])

    def to_dict(self):
        return asdict(self)

    @classmethod
    def from_dict(cls, d):
        return cls(
            d["kind"],
            d["category"],
            float(d["amount"]),
            d.get("note", ""),
            d.get("date", datetime.now().strftime("%Y-%m-%d")),
            d.get("tid", uuid.uuid4().hex[:8]),
        )


class BudgetTracker:
    def __init__(self):
        self.transactions: List[Transaction] = []

    def add(self, kind, category, amount, note=""):
        if kind not in ("expense", "income"):
            raise ValueError("kind must be 'expense' or 'income'")
        if amount <= 0:
            raise ValueError("amount must be positive")
        t = Transaction(kind, category.strip() or "Uncategorized", round(amount, 2), note)
        self.transactions.append(t)
        return t

    def remove(self, tid):
        for i, t in enumerate(self.transactions):
            if t.tid == tid:
                return self.transactions.pop(i)
        return None

    def total(self, kind):
        return round(sum(t.amount for t in self.transactions if t.kind == kind), 2)

    def balance(self):
        return round(self.total("income") - self.total("expense"), 2)

    def by_category(self, kind):
        out = {}
        for t in self.transactions:
            if t.kind == kind:
                out[t.category] = round(out.get(t.category, 0.0) + t.amount, 2)
        return dict(sorted(out.items(), key=lambda kv: -kv[1]))

    def savings_rate(self):
        inc = self.total("income")
        if inc <= 0:
            return 0.0
        return round((inc - self.total("expense")) / inc * 100, 1)