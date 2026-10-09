'''
move.py
Represents a single chess move with origin/destination squares, the moving
piece, optional capture, castling side, en-passant flag and promotion piece.
'''
class Move:
    def __init__(self, origin, destination, piece, captured=None,
                 is_castling=None, is_en_passant=False, promotion=None,
                 is_double_push=False):
        self.origin = origin              # (row, col) tuple
        self.destination = destination    # (row, col) tuple
        self.piece = piece                # Piece object being moved
        self.captured = captured          # Piece object captured (may be None)
        self.is_castling = is_castling    # None, 'K' (kingside) or 'Q' (queenside)
        self.is_en_passant = is_en_passant
        self.promotion = promotion        # 'Q', 'R', 'B' or 'N' or None
        self.is_double_push = is_double_push
    def __repr__(self):
        ...