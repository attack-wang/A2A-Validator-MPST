'''
exceptions.py
Custom exception types for the Checkers game.
'''
class CheckersError(Exception):
    """Base class for all custom Checkers game errors."""
class InvalidNotationError(CheckersError):
    """Raised when a move string cannot be parsed (bad notation format)."""
class InvalidMoveError(CheckersError):
    """Raised when a syntactically valid move violates the game rules."""
class QuitGameError(CheckersError):
    """Raised internally when a player chooses to quit the game."""