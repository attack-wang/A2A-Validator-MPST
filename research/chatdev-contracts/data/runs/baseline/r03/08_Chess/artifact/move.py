'''
Move class representing a chess move with all metadata needed for
execution, undo, and notation generation.
'''
class Move:
    def __init__(self, start, end, piece, captured=None, is_en_passant=False,
                 is_castling=False, promotion=None, rook_start=None, rook_end=None):
        self.start = start        # (row, col)
        self.end = end            # (row, col)
        self.piece = piece        # Piece object being moved
        self.captured = captured  # Piece object captured (None if none)
        self.is_en_passant = is_en_passant
        self.is_castling = is_castling
        self.promotion = promotion  # Piece subclass for promotion
        self.rook_start = rook_start  # for castling
        self.rook_end = rook_end
        # state saved for undo
        self.prev_has_moved = None
        self.prev_rook_has_moved = None
        self.prev_en_passant_target = None
        self.promotion_options = []
    def __eq__(self, other):
        if not isinstance(other, Move):
            return NotImplemented
        return (self.start == other.start and self.end == other.end
                and self.piece is other.piece
                and self.promotion == other.promotion)
    def __repr__(self):
        return f"Move({self.start}->{self.end})"