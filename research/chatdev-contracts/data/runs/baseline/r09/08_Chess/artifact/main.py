class Move:
    def __init__(self, from_sq, to_sq, piece, captured=None, promotion=None, flag=None):
        self.from_file, self.from_rank = from_sq
        self.to_file, self.to_rank = to_sq
        self.piece = piece
        self.captured = captured
        self.promotion = promotion
        self.is_castling = None  # 'K' or 'Q'
        self.is_en_passant = False
        self.is_double_push = False
        if flag == 'K' or flag == 'Q':
            self.is_castling = flag
        elif flag == 'ep':
            self.is_en_passant = True
        elif flag == 'double':
            self.is_double_push = True
    @property
    def from_sq(self):
        return (self.from_file, self.from_rank)
    @property
    def to_sq(self):
        return (self.to_file, self.to_rank)
    def __repr__(self):
        return f"Move({self.from_sq}->{self.to_sq})"