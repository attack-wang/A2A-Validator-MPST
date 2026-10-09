'''
position.py
Represents a square on the 8x8 checkers board using 0-based internal
(row, col) coordinates and algebraic notation ("a1".."h8") for I/O.
'''
from dataclasses import dataclass
@dataclass(frozen=True)
class Position:
    row: int
    col: int
    @classmethod
    def from_notation(cls, text):
        """Parse a square such as 'b3' into a Position (row 0 = rank 8)."""
        text = text.strip().lower()
        if len(text) != 2 or text[0] not in "abcdefgh" or text[1] not in "12345678":
            raise ValueError(f"Invalid position: {text!r}")
        col = ord(text[0]) - ord("a")
        row = 8 - int(text[1])
        return cls(row, col)
    def notation(self):
        """Return the algebraic notation of this square, e.g. 'b3'."""
        return f"{'abcdefgh'[self.col]}{8 - self.row}"
    def __str__(self):
        return self.notation()