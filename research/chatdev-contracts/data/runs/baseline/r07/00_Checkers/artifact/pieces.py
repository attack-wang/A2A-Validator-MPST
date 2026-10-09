'''
pieces.py - Piece definitions for the Checkers game.
Defines the two player colors (RED, BLACK) and the Piece class,
including king promotion and display symbols:
  r / b  = ordinary men,  R / B = kings.
'''
RED = "Red"
BLACK = "Black"
class Piece:
    """A single checkers piece (man or king) belonging to RED or BLACK."""
    def __init__(self, color, is_king=False):
        self.color = color
        self.is_king = is_king
    def promote(self):
        """Crown this piece, turning it into a king."""
        self.is_king = True
    @property
    def symbol(self):
        """Single-character board symbol: 'r'/'b' for men, 'R'/'B' for kings."""
        base = 'r' if self.color == RED else 'b'
        return base.upper() if self.is_king else base
    def __repr__(self):
        return "Piece(color={}, is_king={})".format(self.color, self.is_king)