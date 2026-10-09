'''
exceptions.py
Custom exception types shared across the Connect Four project. Keeping
them in a dedicated module lets the Board (rule enforcement) and the
Game (input handling) layers raise and catch precise, meaningful errors
without any circular imports. This module is the SINGLE source of truth
for every custom exception in the project.
'''
class InvalidColumnError(Exception):
    """Raised when a typed column choice is not an integer from 1 to 7."""
    def __init__(self, column):
        """Store the offending value so callers can report it clearly."""
        self.column = column
        super().__init__(
            f"Invalid column: {column!r}. Please type a number between 1 and 7."
        )
class ColumnFullError(Exception):
    """Raised when the chosen column already holds six discs."""
    def __init__(self, column):
        """Store the offending column index for clearer error messages."""
        self.column = column
        super().__init__(f"Column {column} is already full. Pick another one.")