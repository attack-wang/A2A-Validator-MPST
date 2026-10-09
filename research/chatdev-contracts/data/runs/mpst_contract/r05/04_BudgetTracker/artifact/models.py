from dataclasses import dataclass, asdict


@dataclass
class Transaction:
    id: int
    date: str
    ttype: str
    category: str
    description: str
    amount: float

    def to_dict(self):
        return asdict(self)

    @classmethod
    def from_dict(cls, d):
        return cls(**d)


@dataclass
class SavingsGoal:
    name: str
    target: float
    saved: float = 0.0

    def to_dict(self):
        return asdict(self)

    @classmethod
    def from_dict(cls, d):
        return cls(**d)