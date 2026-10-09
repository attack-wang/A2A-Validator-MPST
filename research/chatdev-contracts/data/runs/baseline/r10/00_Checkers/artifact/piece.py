'''
piece.py
Defines the Piece and PieceColor entities used across the game.
A piece has a color (RED or BLACK) and a king flag. Men move/capture
forward only; kings move/capture in all four diagonal directions.
'''
from enum import Enum
class PieceColor(Enum):
    RED = "r"
    BLACK = "b"
    @property
    def name_str(self):
        """Human-readable color name for prompts and messages."""
        return "Red" if self is PieceColor.RED else "Black"
    @property
    def forward(self):
        """Row delta for forward movement (Red moves up the board / decreasing row index)."""
        return -1 if self is PieceColor.RED else 1
    @property
    def king_row(self):
        """Row index where pieces of this color get crowned."""
        return 0 if self is PieceColor.RED else 7
    @property
    def opponent(self):
        """The opposite color."""
        return PieceColor.BLACK if self is PieceColor.RED else PieceColor.RED
class Piece:
    """A single checkers man/king."""
    def __init__(self, color):
        self.color = color
        self.is_king = False
    def crown(self):
        """Promote this piece to a king."""
        self.is_king = True
    @property
    def symbol(self):
        """Lowercase letter for a man, uppercase for a king."""
        base = self.color.value
        return base.upper() if self.is_king else base
    def move_directions(self):
        """Diagonal step directions available for normal (non-capturing) moves."""
        if self.is_king:
            return [(-1, -1), (-1, 1), (1, -1), (1, 1)]
        f = self.color.forward
        return [(f, -1), (f, 1)]
    def capture_directions(self):
        """English/American rules: men capture forward only; kings any direction."""
        return self.move_directions()
    def copy(self):
        """Return an independent copy of this piece (preserves king flag)."""
        clone = Piece(self.color)
        clone.is_king = self.is_king
        return clone
    def __str__(self):
        return self.symbol
    def __repr__(self):
        return f"Piece({self.color.name_str}, king={self.is_king})"