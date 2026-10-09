'''
game_logic.py — difficulty presets (label, rows, cols, mine count) for Minesweeper.
'''
from enum import Enum
class Difficulty(Enum):
    """The three classic difficulty presets."""
    BEGINNER = ("Beginner", 9, 9, 10)
    INTERMEDIATE = ("Intermediate", 16, 16, 40)
    EXPERT = ("Expert", 16, 30, 99)
    @property
    def label(self):
        """Human-readable difficulty name."""
        return self.value[0]
    @property
    def rows(self):
        """Number of board rows."""
        return self.value[1]
    @property
    def cols(self):
        """Number of board columns."""
        return self.value[2]
    @property
    def mines(self):
        """Number of mines hidden on the board."""
        return self.value[3]
    @property
    def description(self):
        """One-line summary used in the difficulty menu."""
        return f"{self.label} — {self.rows}x{self.cols}, {self.mines} mines"