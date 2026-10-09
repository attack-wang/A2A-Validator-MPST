'''
pieces.py
Defines the Piece class and a factory function create_piece().
A piece stores its color ('w' or 'b'), its type ('K','Q','R','B','N','P'),
and whether it has moved (used for castling rights and pawn double pushes).
'''
class Piece:
    """Represents a single chess piece."""
    def __init__(self, color, piece_type):
        self.color = color          # 'w' (white) or 'b' (black)
        self.type = piece_type      # 'K','Q','R','B','N','P'
        self.has_moved = False      # True once the piece has moved at least once
    @property
    def symbol(self):
        """Uppercase for white, lowercase for black (used for board printing)."""
        return self.type if self.color == 'w' else self.type.lower()
    def __repr__(self):
        return self.symbol
def create_piece(piece_type, color):
    """Factory: build a Piece from a type char ('K','Q','R','B','N','P') and color ('w'/'b')."""
    return Piece(color, piece_type.upper())