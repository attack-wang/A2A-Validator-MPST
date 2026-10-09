'''
savings_goal.py
Defines the SavingsGoal model used to track progress toward a
target amount of savings.
'''
class SavingsGoal:
    """Represents a named savings target with progress tracking."""
    def __init__(self, name, target_amount, current_amount=0.0):
        if target_amount <= 0:
            raise ValueError("Target amount must be positive.")
        if current_amount < 0:
            raise ValueError("Current amount cannot be negative.")
        self.name = name.strip()
        self.target_amount = round(float(target_amount), 2)
        self.current_amount = round(float(current_amount), 2)
    def deposit(self, amount):
        """Add a positive amount to the current savings."""
        if amount <= 0:
            raise ValueError("Deposit must be positive.")
        self.current_amount = round(self.current_amount + amount, 2)
    def withdraw(self, amount):
        """Remove a positive amount, refusing to overdraw the goal."""
        if amount <= 0:
            raise ValueError("Withdrawal must be positive.")
        if amount > self.current_amount:
            raise ValueError("Withdrawal exceeds current savings.")
        self.current_amount = round(self.current_amount - amount, 2)
    @property
    def remaining(self):
        return round(max(self.target_amount - self.current_amount, 0.0), 2)
    @property
    def percent_complete(self):
        return round(min(self.current_amount / self.target_amount * 100, 100.0), 1)
    @property
    def is_complete(self):
        return self.current_amount >= self.target_amount
    def to_dict(self):
        return {
            "name": self.name,
            "target_amount": self.target_amount,
            "current_amount": self.current_amount,
        }
    @classmethod
    def from_dict(cls, data):
        return cls(
            name=data.get("name", "Unnamed Goal"),
            target_amount=data.get("target_amount", 1.0),
            current_amount=data.get("current_amount", 0.0),
        )
    def __str__(self):
        bar = "#" * int(round(self.percent_complete / 5))
        mark = " [COMPLETE]" if self.is_complete else ""
        return (f"{self.name:<18} ${self.current_amount:>10,.2f} / "
                f"${self.target_amount:>10,.2f}  {self.percent_complete:5.1f}% {bar}{mark}")