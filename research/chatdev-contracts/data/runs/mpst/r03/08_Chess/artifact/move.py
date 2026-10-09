'''
move.py
Represents a single chess move: start/end squares, moving piece, captured
piece, promotion piece, and flags for castling, en passant, double pawn push.
'''
class Move:
    """Represents a single chess move."""
    __slots__ = ('start', 'end', 'piece', 'captured', 'promotion',
                 'is_castling', 'is_en_passant', 'is_double_pawn')
    def __init__(self, start, end, piece, captured=None, promotion=None,
                 is_castling=None, is_en_passant=False, is_double_pawn=False):
        """
        start/end: (row, col) tuples, row 0 = rank 8.
        piece: the moving Piece object.
        captured: the captured Piece object or None.
        promotion: piece type letter ('Q','R','B','N') or None.
        is_castling: 'K' for kingside, 'Q' for queenside, None otherwise.
        is_en_passant: True if this is an en passant capture.
        is_double_pawn: True if pawn advanced two squares.
        """
        self.start = start
        self.end = end
        self.piece = piece
        self.captured = captured
        self.promotion = promotion
        self.is_castling = is_castling
        self.is_en_passant = is_en_passant
        self.is_double_pawn = is_double_pawn
    def __repr__(self):
        ...