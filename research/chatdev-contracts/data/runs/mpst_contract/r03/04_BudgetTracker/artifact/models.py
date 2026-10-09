from dataclasses import dataclass


@dataclass
class Transaction:
    id: str
    date: str
    kind: str  # "income" or "expense"
    category: str
    description: str
    amount: float


@dataclass
class SavingsGoal:
    name: str
    target: float
    saved: float = 0.0

    @property
    def progress(self):
        return min(100.0, self.saved / self.target * 100) if self.target > 0 else 0.0