'''Data models for the crossword puzzle: directions, cells, entries and errors.'''
from enum import Enum
class Direction(Enum):
    ACROSS = "across"
    DOWN = "down"
    @classmethod
    def from_string(cls, text):
        """Parse 'across'/'a'/'down'/'d' (case-insensitive) into a Direction."""
        if not isinstance(text, str):
            raise CrosswordError(f"Direction must be a string, got {type(text).__name__!r}.")
        normalized = text.strip().lower()
        if normalized in ("across", "a", "->", "ac"):
            return cls.ACROSS
        if normalized in ("down", "d", "|", "dn"):
            return cls.DOWN
        raise CrosswordError(f"Unknown direction {text!r}; use 'across'/'a' or 'down'/'d'.")
    @property
    def label(self):
        return self.value.capitalize()  # "Across" / "Down"