'''Move representation for chess.'''
class Move:
    __slots__ = ('from_sq', 'to_sq', 'piece', 'captured', 'is_en_passant',
                 'castle', 'promotion', 'is_double_push')
    def __init__(self, from_sq, to_sq, piece, captured=None, is_en_passant=False,
                 castle=None, promotion=None, is_double_push=False):
        self.from_sq = from_sq
        self.to_sq = to_sq
        self.piece = piece
        self.captured = captured
        self.is_en_passant = is_en_passant
        self.castle = castle
        self.promotion = promotion
        self.is_double_push = is_double_push
    def __eq__(self, other):
        if not isinstance(other, Move):
            return NotImplemented
        return (self.from_sq == other.from_sq and
                self.to_sq == other.to_sq and
                self.promotion == other.promotion and
                self.castle == other.castle)
    def __hash__(self):
        return hash((self.from_sq, self.to_sq, self.promotion, self.castle))
    def __repr__(self):
        ...