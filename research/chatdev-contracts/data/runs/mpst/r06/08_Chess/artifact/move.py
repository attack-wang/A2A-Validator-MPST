'''Move representation for the chess game.'''
class Move:
    """Represents a single chess move with all metadata needed for
    application, SAN generation and undo."""
    __slots__ = ('start', 'end', 'piece', 'captured', 'promotion',
                 'is_castle_king', 'is_castle_queen', 'is_en_passant')
    def __init__(self, start, end, piece, captured=None, promotion=None,
                 is_castle_king=False, is_castle_queen=False, is_en_passant=False):
        self.start = start          # (row, col) with row 0 = rank 8
        self.end = end              # (row, col)
        self.piece = piece          # Piece being moved
        self.captured = captured    # Piece captured or None
        self.promotion = promotion  # 'Q', 'R', 'B', 'N' or None
        self.is_castle_king = is_castle_king
        self.is_castle_queen = is_castle_queen
        self.is_en_passant = is_en_passant
    def __repr__(self):
        return f"<Move {self.piece.type} {self.start}->{self.end}" + ...