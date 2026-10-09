'''
exceptions.py
Custom exception types for Connect Four move validation.
'''
class ConnectFourError(Exception):
    """Base class for all Connect Four game errors."""
class InvalidColumnError(ConnectFourError):
    """Raised when a chosen column is outside the range 1..7."""
class ColumnFullError(ConnectFourError):
    """Raised when a chosen column already contains six discs."""