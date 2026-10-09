'''
piece.py
Defines the Piece class and the PieceColor enumeration used to represent
the checkers pieces on the board.
A piece knows its color (RED or BLACK) and whether it has been crowned
as a king.  Kings may move and capture diagonally in all four
directions, while ordinary men may only move/capture forward.
'''
from enum import Enum
class PieceColor(Enum):
    """Enumeration of the two players' piece colors."""
    RED = "red"
    BLACK = "black"
    @property
    def opposite(self):
        """Return the opposing color."""
        return PieceColor.BLACK if self is PieceColor.RED else PieceColor.RED
class Piece:
    """A single checkers man (or king) belonging to one of the players."""
    def __init__(self, color, is_king=False):
        self._color = color
        self._is_king = is_king
    @property
    def color(self):
        return self._color
    @property
    def is_king(self):
        return self._is_king
    def crown(self):
        """Promote this piece to a king."""
        self._is_king = True
    @property
    def symbol(self):
        """Single-character symbol used when rendering the board."""
        base = 'r' if self._color is PieceColor.RED else 'b'
        return base.upper() if self._is_king else base
    def __str__(self):
        return self.symbol
    def __repr__(self):
        return f"Piece({self._color.value}, king={self._is_king})"