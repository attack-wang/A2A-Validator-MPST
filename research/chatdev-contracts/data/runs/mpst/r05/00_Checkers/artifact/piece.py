'''
piece.py
Defines the Piece class used by the Checkers board.
A Piece knows:
  * its color ('r' for red, 'b' for black)
  * whether it has been crowned (is a king)
Display convention:
  * 'r' / 'b'  -> ordinary man
  * 'R' / 'B'  -> king
'''
class Piece:
    """A single checkers man or king."""
    def __init__(self, color, is_king=False):
        """Create a piece of the given color ('r' or 'b'); optionally a king."""
        if color not in ('r', 'b'):
            raise ValueError("Piece color must be 'r' or 'b'")
        self._color = color
        self._is_king = is_king
    @property
    def color(self):
        """Return the piece's color: 'r' (red) or 'b' (black)."""
        return self._color
    @property
    def is_king(self):
        """Return True if the piece has been crowned (is a king)."""
        return self._is_king
    def make_king(self):
        """Crown this piece so it may move and capture in all directions."""
        self._is_king = True
    def directions(self):
        """Return the (dr, dc) diagonal directions this piece may travel.
        Men move/capture only forward (red toward rank 8, black toward rank 1);
        kings move/capture in all four diagonal directions.
        """
        if self._is_king:
            return [(-1, -1), (-1, 1), (1, -1), (1, 1)]
        if self._color == 'r':      # red sits at the bottom and moves up
            return [(-1, -1), (-1, 1)]
        return [(1, -1), (1, 1)]    # black sits at the top and moves down
    def __repr__(self):
        """Return the one-character symbol: 'r'/'R'/'b'/'B' (uppercase = king)."""
        symbol = 'r' if self._color == 'r' else 'b'
        return symbol.upper() if self._is_king else symbol
    def __str__(self):
        """Human-readable symbol used when rendering the board."""
        return repr(self)