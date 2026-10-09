@dataclass
class CategoryBudget:
    """A monthly spending limit for one expense category."""
    name: str
    monthly_limit: float
    def __post_init__(self):
        self.name = str(self.name).strip()
        if not self.name:
            raise ValueError("Budget category cannot be empty.")
        try:
            self.monthly_limit = round(float(self.monthly_limit), 2)
        except (TypeError, ValueError):
            raise ValueError(f"Monthly limit must be a number, got {self.monthly_limit!r}")
        if self.monthly_limit <= 0:
            raise ValueError("Monthly limit must be greater than zero.")
    def to_dict(self) -> dict:
        return {"name": self.name, "monthly_limit": self.monthly_limit}
    @classmethod
    def from_dict(cls, data: dict) -> "CategoryBudget":
        return cls(name=data["name"], monthly_limit=data["monthly_limit"])