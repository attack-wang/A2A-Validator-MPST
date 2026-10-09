'''
Move record: start/end squares, flags for castling, en passant, promotion.
'''
class Move:
    """Represents a chess move."""
    def __init__(self, start, end, piece, captured=None, promotion=None,
                 is_castle_king=False, is_castle_queen=False,
                 is_en_passant=False, is_double_push=False):
        self.start = start  # (file, rank)
        self.end = end
        self.piece = piece
        self.captured = captured  # piece object being captured, or None
        self.promotion = promotion  # piece class for promotion, or None
        self.is_castle_king = is_castle_king
        self.is_castle_queen = is_castle_queen
        self.is_en_passant = is_en_passant
        self.is_double_push = is_double_push
    @property
    def is_capture(self):
        return self.captured is not None or self.is_en_passant
    def __repr__(self):
        return f"Move({self.start}->{self.end})"