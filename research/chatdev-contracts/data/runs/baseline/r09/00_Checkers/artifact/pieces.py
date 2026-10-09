'''
pieces.py
Defines the Piece entity used on the checkers board.
A piece has a color (RED or BLACK) and a king flag. Men move/capture
forward only; kings move/capture in all four diagonal directions.
'''
from enum import Enum
class PieceColor(Enum):
    RED = "Red"
    BLACK = "Black"
    @property
    def opponent(self):
        return PieceColor.BLACK if self is PieceColor.RED else PieceColor.RED
class Piece:
    """A single checkers man or king."""
    def __init__(self, color):
        self.color = color
        self.is_king = False
    def crown(self):
        """Promote this man to a king."""
        self.is_king = True
    def copy(self):
        """Return an independent copy of this piece (preserves king status)."""
        new = Piece(self.color)
        new.is_king = self.is_king
        return new
    @property
    def symbol(self):
        """Uppercase for RED, lowercase for BLACK; kings shown doubled."""
        if self.color is PieceColor.RED:
            return 'R' if self.is_king else 'r'
        return 'B' if self.is_king else 'b'