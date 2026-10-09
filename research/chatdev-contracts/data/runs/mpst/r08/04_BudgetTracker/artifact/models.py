'''
Data models for the Budget Tracker application.
Defines the Transaction and SavingsGoal classes that represent
the core domain objects used throughout the application.
'''
class Transaction:
    """Represents a single income or expense transaction."""
    def __init__(self, transaction_id, date, category, description, amount, transaction_type):
        self.transaction_id = transaction_id
        self.date = date
        self.category = category
        self.description = description
        self.amount = amount
        self.transaction_type = transaction_type  # 'Expense' or 'Income'
    def to_tuple(self):
        """Return the transaction as a tuple for database operations."""
        return (self.date, self.category, self.description, self.amount, self.transaction_type)
    def __str__(self):
        return f"[{self.transaction_id}] {self.date} | {self.transaction_type} | {self.category} | ${self.amount:.2f} | {self.description}"
class SavingsGoal:
    """Represents a savings goal with a target amount and progress."""
    def __init__(self, goal_id, name, target_amount, current_amount, deadline):
        self.goal_id = goal_id
        self.name = name
        self.target_amount = target_amount
        self.current_amount = current_amount
        self.deadline = deadline
    def progress(self):
        """Return the progress toward the goal as a percentage (0-100)."""
        if self.target_amount <= 0:
            return 0.0
        return min(100.0, (self.current_amount / self.target_amount) * 100.0)
    def remaining(self):
        """Return the amount remaining to reach the goal."""
        return max(0.0, self.target_amount - self.current_amount)