'''
pieces.py
Defines chess piece types, their colors, symbols, and movement direction constants.
'''
KNIGHT_OFFSETS = [(1, 2), (2, 1), (2, -1), (1, -2), (-1, -2), (-2, -1), (-2, 1), (-1, 2)]
BISHOP_DIRS = [(1, 1), (1, -1), (-1, 1), (-1, -1)]
ROOK_DIRS = [(1, 0), (-1, 0), (0, 1), (0, -1)]
KING_DIRS = BISHOP_DIRS + ROOK_DIRS
class Piece:
    """Represents a chess piece with a color and a type."""
    WHITE = 'w'
    BLACK = 'b'
    NAMES = {
        'K': 'King',
        'Q': 'Queen',
        'R': 'Rook',
        'B': 'Bishop',
        'N': 'Knight',
        'P': 'Pawn',
    }
    def __init__(self, color, kind):
        self.color = color
        self.kind = kind
    @property
    def symbol(self):
        return self.kind if self.color == Piece.WHITE else self.kind.lower()
    @property
    def name(self):
        return Piece.NAMES[self.kind]
    def is_white(self):
        return self.color == Piece.WHITE
    def __repr__(self):
        return f"Piece({self.color!r}, {self.kind!r})"
    def __eq__(self, other):
        return isinstance(other, Piece) and self.color == other.color and self.kind == other.kind
    def __hash__(self):
        return hash((self.color, self.kind))