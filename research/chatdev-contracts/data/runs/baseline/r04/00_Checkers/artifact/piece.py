'''
piece.py
Defines the Piece class and the PieceColor enumeration used to represent
the checkers pieces on the board.
A Piece knows:
  * its color (PieceColor.RED or PieceColor.BLACK)
  * whether it has been crowned a king
  * which diagonal directions it may step/jump in (men move forward only,
    kings move in all four diagonal directions)
  * its single-character symbol used when rendering the board
'''
from enum import Enum
class PieceColor(Enum):
    """The two sides of a checkers game."""
    RED = "Red"
    BLACK = "Black"
    @property
    def opponent(self):
        """Return the opposite color."""
        return PieceColor.BLACK if self is PieceColor.RED else PieceColor.RED
    @property
    def symbol(self):
        """Lowercase letter used to identify this color on the board."""
        return "r" if self is PieceColor.RED else "b"
class Piece:
    """A single checkers man (or king) belonging to one of the two colors."""
    def __init__(self, color):
        self._color = color
        self._is_king = False
    @property
    def color(self):
        return self._color
    @property
    def is_king(self):
        return self._is_king
    def crown(self):
        """Promote this man to a king (no effect if already a king)."""
        self._is_king = True
    @property
    def symbol(self):
        """Board symbol: lowercase for a man, uppercase for a king."""
        s = self._color.symbol
        return s.upper() if self._is_king else s
    def directions(self):
        """
        Diagonal step directions (dr, dc) available to this piece.
        Red starts at the bottom of the board and moves toward row 0
        (dr = -1); Black starts at the top and moves toward row 7 (dr = +1).
        Kings may move in all four diagonal directions.
        """
        if self._is_king:
            return ((-1, -1), (-1, 1), (1, -1), (1, 1))
        if self._color is PieceColor.RED:
            return ((-1, -1), (-1, 1))
        return ((1, -1), (1, 1))
    def __repr__(self):
        return f"Piece({self._color.value}, king={self._is_king})"