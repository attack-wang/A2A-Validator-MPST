from dataclasses import dataclass, field, asdict


@dataclass
class Transaction:
    date: str
    category: str
    description: str
    amount: float
    ttype: str  # "expense" or "income"

    def to_dict(self):
        return asdict(self)

    @staticmethod
    def from_dict(d):
        return Transaction(
            date=d["date"],
            category=d["category"],
            description=d["description"],
            amount=float(d["amount"]),
            ttype=d["ttype"],
        )


@dataclass
class Budget:
    monthly_income_goal: float = 0.0
    savings_goal: float = 0.0
    category_limits: dict = field(default_factory=dict)

    def to_dict(self):
        return {
            "monthly_income_goal": self.monthly_income_goal,
            "savings_goal": self.savings_goal,
            "category_limits": self.category_limits,
        }

    @staticmethod
    def from_dict(d):
        return Budget(
            monthly_income_goal=float(d.get("monthly_income_goal", 0.0)),
            savings_goal=float(d.get("savings_goal", 0.0)),
            category_limits=dict(d.get("category_limits", {})),
        )