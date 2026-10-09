class SavingsGoal:
    """A named savings target with progress tracking."""
    def __init__(self, name, target_amount, saved_amount=0.0, goal_id=None):
        if target_amount is None or float(target_amount) <= 0:
            raise ValueError("Savings target must be a positive number.")
        if saved_amount is None or float(saved_amount) < 0:
            raise ValueError("Saved amount must be a non-negative number.")
        self.id = goal_id if goal_id else str(uuid.uuid4())
        self.name = name
        self.target_amount = round(float(target_amount), 2)
        self.saved_amount = round(float(saved_amount), 2)
    @property
    def progress(self):
        """Percentage of the goal completed (0-100)."""
        if self.target_amount <= 0:
            return 0.0
        return min(self.saved_amount / self.target_amount * 100.0, 100.0)
    @property
    def remaining(self):
        """Amount still needed to reach the target."""
        return max(self.target_amount - self.saved_amount, 0.0)
    @property
    def is_complete(self):
        """True when the saved amount has reached the target."""
        return self.saved_amount >= self.target_amount
    def deposit(self, amount):
        """Add money to the goal."""
        amount = float(amount)
        if amount <= 0:
            raise ValueError("Deposit must be a positive number.")
        self.saved_amount = round(self.saved_amount + amount, 2)
    def withdraw(self, amount):
        """Remove money from the goal (cannot go below zero)."""
        amount = float(amount)
        if amount <= 0:
            raise ValueError("Withdrawal must be a positive number.")
        if amount > self.saved_amount:
            raise ValueError(
                f"Cannot withdraw {amount:.2f}; only {self.saved_amount:.2f} saved."
            )
        self.saved_amount = round(self.saved_amount - amount, 2)
    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "target_amount": self.target_amount,
            "saved_amount": self.saved_amount,
        }
    @classmethod
    def from_dict(cls, data):
        return cls(
            name=data.get("name", "Goal"),
            target_amount=data.get("target_amount", 1.0),
            saved_amount=data.get("saved_amount", 0.0),
            goal_id=data.get("id"),
        )
    def __repr__(self):
        return f"SavingsGoal({self.name}, {self.saved_amount:.2f}/{self.target_amount:.2f})"