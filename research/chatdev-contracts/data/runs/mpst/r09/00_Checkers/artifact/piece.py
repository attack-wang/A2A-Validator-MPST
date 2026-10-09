'''
piece.py
Defines the Piece class and PieceColor enum used to populate the board.
'''
from enum import Enum
class PieceColor(Enum):
    """The two opposing colors in the game."""
    RED = "r"
    BLACK = "b"
    @property
    def opposite(self):
        return PieceColor.BLACK if self is PieceColor.RED else PieceColor.RED
class Piece:
    """A single checkers man or king."""
    def __init__(self, color):
        self.color = color
        self.is_king = False
    def crown(self):
        """Promote this piece to a king."""
        self.is_king = True
    @property
    def symbol(self):
        """Single-character symbol used when rendering the board."""
        base = self.color.value  # 'r' or 'b'
        return base.upper() if self.is_king else base
    def forward_directions(self):
        """Diagonal (dr, dc) directions a man of this color may move."""
        if self.color is PieceColor.RED:
            return [(1, -1), (1, 1)]
        return [(-1, -1), (-1, 1)]
    def all_directions(self):
        """All four diagonal directions (used by kings)."""
        return [(1, -1), (1, 1), (-1, -1), (-1, 1)]
    def directions(self):
        return self.all_directions() if self.is_king else self.forward_directions()
    def __repr__(self):
        return f"Piece({self.color.name}, {'king' if self.is_king else 'man'})"