'''
exceptions.py
Custom exception types for the Connect Four game. These allow the Board
to signal invalid disc placements in a precise way that the Game loop
can report to the players.
'''
class ConnectFourError(Exception):
    """Base class for all Connect Four game errors."""
    pass
class InvalidColumnError(ConnectFourError):
    """Raised when a chosen column index is outside the valid range."""
    pass
class ColumnFullError(ConnectFourError):
    """Raised when a chosen column has no empty cells remaining."""
    pass