class Move:
    def __init__(self, from_row, from_col, to_row, to_col, piece, captured=None,
                 promotion=None, is_en_passant=False, is_castle=None, is_double_push=False):
        self.from_row = from_row
        self.from_col = from_col
        self.to_row = to_row
        self.to_col = to_col
        self.piece = piece
        self.captured = captured
        self.promotion = promotion  # piece letter 'Q','R','B','N' or piece object?
        self.is_en_passant = is_en_passant
        self.is_castle = is_castle  # 'K' or 'Q'
        self.is_double_push = is_double_push
        self.san = ''