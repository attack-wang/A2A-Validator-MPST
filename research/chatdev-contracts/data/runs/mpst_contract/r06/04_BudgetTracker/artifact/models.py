from dataclasses import dataclass


@dataclass
class Transaction:
    id: int
    date: str
    kind: str  # expense | income | savings
    category: str
    description: str
    amount: float

    def to_dict(self):
        return {
            "id": self.id,
            "date": self.date,
            "kind": self.kind,
            "category": self.category,
            "description": self.description,
            "amount": self.amount,
        }

    @staticmethod
    def from_dict(d):
        return Transaction(int(d["id"]), str(d["date"]), str(d["kind"]),
                           str(d["category"]), str(d["description"]), float(d["amount"]))