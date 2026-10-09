@dataclass
class SavingsGoal:
    """A named savings target, e.g. 'Emergency Fund' with a $5,000 target."""
    name: str
    target_amount: float
    deadline: Optional[str] = None
    id: str = field(default_factory=_generate_id)
    def __post_init__(self):
        self.name = str(self.name).strip()
        if not self.name:
            raise ValueError("Goal name cannot be empty.")
        try:
            self.target_amount = round(float(self.target_amount), 2)
        except (TypeError, ValueError):
            raise ValueError(f"Target amount must be a number, got {self.target_amount!r}")
        if self.target_amount <= 0:
            raise ValueError("Target amount must be greater than zero.")
        if self.deadline in ("", None):
            self.deadline = None
        elif not is_valid_date(self.deadline):
            raise ValueError(f"Deadline must be YYYY-MM-DD, got {self.deadline!r}")
    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "name": self.name,
            "target_amount": self.target_amount,
            "deadline": self.deadline,
        }
    @classmethod
    def from_dict(cls, data: dict) -> "SavingsGoal":
        return cls(
            name=data["name"],
            target_amount=data["target_amount"],
            deadline=data.get("deadline"),
            id=data.get("id", _generate_id()),
        )