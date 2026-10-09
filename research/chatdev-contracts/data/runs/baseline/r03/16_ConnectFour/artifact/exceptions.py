'''
Custom exceptions for the Connect Four game.
These exceptions signal invalid move attempts so the game loop can
re-prompt the player for input instead of crashing.
'''
class ConnectFourError(Exception):
    """Base class for all Connect Four game errors."""
class InvalidColumnError(ConnectFourError):
    """Raised when a chosen column is outside the valid 1-7 range."""
class ColumnFullError(ConnectFourError):
    """Raised when a chosen column already contains six discs."""