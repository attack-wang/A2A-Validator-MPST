class SavingsGoal:
    """A named savings target with progress tracking."""
    def __init__(self, name, target_amount, current_amount=0.0,
                 deadline=None, goal_id=None):
        self.id = goal_id if goal_id is not None else str(uuid.uuid4())
        self.name = name
        self.target_amount = round(float(target_amount), 2)
        self.current_amount = round(float(current_amount), 2)
        self.deadline = deadline  # "YYYY-MM-DD" or None
    def add_contribution(self, amount):
        self.current_amount = round(self.current_amount + float(amount), 2)
    def progress(self):
        if self.target_amount <= 0:
            return 0.0
        return min(100.0, (self.current_amount / self.target_amount) * 100.0)
    def is_complete(self):
        return self.current_amount >= self.target_amount
    def to_dict(self): ...
    @classmethod
    def from_dict(cls, data): ...