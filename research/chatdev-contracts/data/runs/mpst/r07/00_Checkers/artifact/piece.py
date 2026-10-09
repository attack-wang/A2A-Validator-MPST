'''
Defines the Piece class and Color enumeration used throughout the Checkers game.
'''
from enum import Enum
class Color(Enum):
    """The two sides of the game."""
    RED = "Red"
    BLACK = "Black"
    @property
    def opposite(self):
        return Color.BLACK if self is Color.RED else Color.RED
class Piece:
    """A single checkers man/king."""
    __slots__ = ("color", "is_king")
    def __init__(self, color, is_king=False):
        self.color = color
        self.is_king = is_king
    def crown(self):
        """Crown this piece as a king."""
        self.is_king = True
    @property
    def symbol(self):
        """Single-character symbol: 'r'/'R' red man/king, 'b'/'B' black man/king."""
        if self.color is Color.RED:
            return 'R' if self.is_king else 'r'
        return 'B' if self.is_king else 'b'
    def copy(self):
        return Piece(self.color, self.is_king)
    def __repr__(self):
        return f"Piece({self.color.value}, king={self.is_king})"
    def __str__(self):
        return self.symbol