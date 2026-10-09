'''
pieces.py
Defines the Piece class and colour constants used across the chess engine.
A piece is a lightweight value object described by:
  * color      : 'w' (White) or 'b' (Black)
  * piece_type : one of 'P', 'N', 'B', 'R', 'Q', 'K'
The class also remembers whether the piece has already moved, which is
required to implement castling rights and pawn double advances correctly.
'''
WHITE = 'w'
BLACK = 'b'
PIECE_VALUES = {'P': 1, 'N': 3, 'B': 3, 'R': 5, 'Q': 9, 'K': 0}
def opposite(color):
    """Return the opposing colour of `color`."""
    return BLACK if color == WHITE else WHITE
class Piece:
    """Represents a single chess piece."""
    __slots__ = ('color', 'piece_type', 'has_moved')
    def __init__(self, color, piece_type, has_moved=False):
        if color not in (WHITE, BLACK):
            raise ValueError("piece colour must be 'w' or 'b', got %r" % (color,))
        if piece_type not in PIECE_VALUES:
            raise ValueError("piece type must be one of 'PNBRQK', got %r" % (piece_type,))
        self.color = color
        self.piece_type = piece_type
        self.has_moved = has_moved
    def is_type(self, *types):
        """True if the piece is one of the given types, e.g. is_type('R', 'Q')."""
        return self.piece_type in types
    def value(self):
        """Conventional material value of the piece (king = 0)."""
        return PIECE_VALUES[self.piece_type]
    def display_char(self):
        """Uppercase letter for White, lowercase for Black."""
        s = self.piece_type
        return s if self.color == WHITE else s.lower()
    def copy(self):
        """Return an independent copy of this piece preserving has_moved."""
        return Piece(self.color, self.piece_type, self.has_moved)
    @staticmethod
    def create(piece_type, color):
        """Factory: build a fresh piece of the requested type and colour."""
        return Piece(color, piece_type)
    def __eq__(self, other):
        if not isinstance(other, Piece):
            return NotImplemented
        return (self.color == other.color
                and self.piece_type == other.piece_type
                and self.has_moved == other.has_moved)
    def __hash__(self):
        return hash((self.color, self.piece_type, self.has_moved))
    def __repr__(self):
        return "Piece(%r, %r, has_moved=%r)" % (self.color, self.piece_type, self.has_moved)