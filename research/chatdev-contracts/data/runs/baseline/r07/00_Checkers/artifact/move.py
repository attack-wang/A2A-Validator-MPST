'''
move.py - Move representation and algebraic notation helpers.
Squares are addressed as (row, col) with row 0 at the top (rank 8) and
col 0 at the left (file 'a'). Notation examples: 'b6', 'a1'.
'''
from dataclasses import dataclass
from typing import Optional, Tuple
FILES = "abcdefgh"
def square_name(pos):
    """Convert a (row, col) position to algebraic notation, e.g., (2, 1) -> 'b6'."""
    row, col = pos
    return "{}{}".format(FILES[col], 8 - row)
def parse_square(text):
    """Parse algebraic notation like 'b6' into a (row, col) tuple.
    Raises ValueError for malformed input.
    """
    text = text.strip().lower()
    if len(text) != 2 or text[0] not in FILES or text[1] not in "12345678":
        raise ValueError(
            "invalid square '{}' (expected a letter a-h followed by a digit 1-8, e.g., 'b6')".format(text)
        )
    col = FILES.index(text[0])
    row = 8 - int(text[1])
    return (row, col)
@dataclass
class Move:
    """A single move from one square to another, optionally capturing a piece."""
    from_pos: Tuple[int, int]
    to_pos: Tuple[int, int]
    captured_pos: Optional[Tuple[int, int]] = None  # None for simple moves
    @property
    def is_jump(self):
        """True if this move captures an enemy piece."""
        return self.captured_pos is not None
    def notation(self):
        """Human-readable notation, e.g., 'b6-a5' or 'b6xd4' for a capture."""
        sep = "x" if self.is_jump else "-"
        return "{}{}{}".format(square_name(self.from_pos), sep, square_name(self.to_pos))