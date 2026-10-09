'''
piece.py
Defines the Piece class representing a single checkers man or king.
'''
class Piece:
    """A single checkers piece (man or king) belonging to one of two colors."""
    RED = 'red'
    BLACK = 'black'
    def __init__(self, color, is_king=False):
        self.color = color
        self.is_king = is_king
    def promote(self):
        """Crown this piece, turning a man into a king."""
        self.is_king = True
    @property
    def symbol(self):
        """Single-character symbol used when rendering the board."""
        if self.color == Piece.RED:
            return 'R' if self.is_king else 'r'
        return 'B' if self.is_king else 'b'
    def forward_directions(self):
        """Diagonal directions (dr, dc) a man of this color may move/capture."""
        if self.color == Piece.RED:
            return [(-1, -1), (-1, 1)]
        return [(1, -1), (1, 1)]
    def all_directions(self):
        """All four diagonal directions (used by kings)."""
        return [(-1, -1), (-1, 1), (1, -1), (1, 1)]
    def move_directions(self):
        """Directions this piece may use for moves and captures."""
        return self.all_directions() if self.is_king else self.forward_directions()
    def __str__(self):
        return self.symbol