'''
savingsgoal.py
Data model for a savings goal: a named target amount with progress tracking.
Part of the budget tracker application's data models.
'''
import uuid
class SavingsGoal:
    """A savings goal with a target amount and the amount saved so far."""
    def __init__(self, name, target_amount, saved_amount=0.0, note="", goal_id=None):
        self.id = goal_id or uuid.uuid4().hex[:10]
        self.name = str(name).strip() or "Untitled goal"
        self.target_amount = self._validate_amount(target_amount, "Target amount")
        self.saved_amount = self._validate_amount(saved_amount, "Saved amount")
        self.note = str(note)
    @staticmethod
    def _validate_amount(amount, label="Amount"):
        try:
            value = float(amount)
        except (TypeError, ValueError):
            raise ValueError(f"{label} must be a number")
        if value < 0:
            raise ValueError(f"{label} cannot be negative")
        return round(value, 2)
    @property
    def remaining(self):
        """Amount still needed to reach the target (never below zero)."""
        return round(max(0.0, self.target_amount - self.saved_amount), 2)
    @property
    def progress(self):
        """Completion ratio between 0.0 and 1.0."""
        if self.target_amount <= 0:
            return 1.0 if self.saved_amount > 0 else 0.0
        return min(1.0, self.saved_amount / self.target_amount)
    @property
    def is_complete(self):
        return self.saved_amount >= self.target_amount and self.target_amount > 0
    def add_contribution(self, amount):
        """Add money to the goal; returns the new saved amount."""
        value = self._validate_amount(amount, "Contribution")
        self.saved_amount = round(self.saved_amount + value, 2)
        return self.saved_amount
    def to_dict(self):
        """Serialise the goal to a plain dictionary."""
        return {
            "id": self.id,
            "name": self.name,
            "target_amount": self.target_amount,
            "saved_amount": self.saved_amount,
            "note": self.note,
        }
    @classmethod
    def from_dict(cls, data):
        """Rebuild a SavingsGoal from its dictionary form."""
        return cls(
            name=data.get("name", "Untitled goal"),
            target_amount=data.get("target_amount", 0.0),
            saved_amount=data.get("saved_amount", 0.0),
            note=data.get("note", ""),
            goal_id=data.get("id"),
        )
    def __repr__(self):
        return f"SavingsGoal({self.name}, saved {self.saved_amount:.2f} / {self.target_amount:.2f})"