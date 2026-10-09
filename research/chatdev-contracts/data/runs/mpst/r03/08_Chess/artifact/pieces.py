'''
pieces.py
Defines color/piece-type constants and the Piece class used by the chess engine.
'''
WHITE = 'w'
BLACK = 'b'
PAWN = 'P'
KNIGHT = 'N'
BISHOP = 'B'
ROOK = 'R'
QUEEN = 'Q'
KING = 'K'
class Piece:
    """A chess piece with a color ('w'/'b') and a type letter ('P','N','B','R','Q','K')."""
    __slots__ = ('color', 'piece_type')
    def __init__(self, color, piece_type):
        self.color = color
        self.piece_type = piece_type
    def __repr__(self):
        # Uppercase for White, lowercase for Black (matches the ASCII board template).
        return self.piece_type if self.color == WHITE else self.piece_type.lower()
    def __eq__(self, other):
        return (isinstance(other, Piece) and
                self.color == other.color and
                self.piece_type == other.piece_type)
    def __hash__(self):
        return hash((self.color, self.piece_type))