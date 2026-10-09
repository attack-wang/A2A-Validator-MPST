from dataclasses import dataclass, field, asdict
from datetime import datetime
import uuid


@dataclass
class Transaction:
    amount: float
    category: str
    tx_type: str  # "expense" or "income"
    note: str = ""
    date: str = field(default_factory=lambda: datetime.now().strftime("%Y-%m-%d"))
    id: str = field(default_factory=lambda: uuid.uuid4().hex[:8])

    def to_dict(self):
        return asdict(self)

    @classmethod
    def from_dict(cls, d):
        return cls(
            amount=float(d["amount"]),
            category=d["category"],
            tx_type=d["tx_type"],
            note=d.get("note", ""),
            date=d.get("date", datetime.now().strftime("%Y-%m-%d")),
            id=d.get("id", uuid.uuid4().hex[:8]),
        )