class Move:
    def __init__(self, start, end, piece, captured=None, promotion=None,
                 is_castle_king_side=False, is_castle_queen_side=False, is_en_passant=False):
        self.start = start  # (row, col)
        self.end = end
        self.piece = piece
        self.captured = captured
        self.promotion = promotion  # piece type char or None
        self.is_castle_king_side = is_castle_king_side
        self.is_castle_queen_side = is_castle_queen_side
        self.is_en_passant = is_en_passant