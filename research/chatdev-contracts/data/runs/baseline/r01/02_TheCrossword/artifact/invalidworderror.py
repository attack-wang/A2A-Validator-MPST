class CrosswordError(Exception):
    """Base class for all crossword-related errors."""
class UnknownEntryError(CrosswordError):
    """Raised when a clue number/direction does not match any entry."""
class InvalidWordError(CrosswordError):
    """Raised when a guessed word is the wrong length or conflicts with the grid."""