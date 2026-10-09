'''
Piece class representing a single checkers man or king.
'''
from constants import PLAYER_SYMBOLS, KING_SYMBOLS
class Piece:
    """A single checkers piece (man or king) belonging to one player."""
    def __init__(self, color):
        self.color = color
        self.is_king = False
    def crown(self):
        """Promote this piece to a king."""
        self.is_king = True
    @property
    def symbol(self):
        """Single-character symbol used on the displayed board."""
        return KING_SYMBOLS[self.color] if self.is_king else PLAYER_SYMBOLS[self.color]
    def __repr__(self):
        return f"Piece(color={self.color!r}, is_king={self.is_king})"