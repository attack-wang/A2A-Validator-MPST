import time
from dataclasses import dataclass, field, asdict


@dataclass
class Transaction:
    kind: str          # "income" or "expense"
    category: str
    amount: float
    note: str = ""
    date: str = field(default_factory=lambda: time.strftime("%Y-%m-%d"))

    def to_dict(self):
        return asdict(self)

    @staticmethod
    def from_dict(d):
        return Transaction(d["kind"], d["category"], float(d["amount"]),
                           d.get("note", ""), d.get("date", ""))