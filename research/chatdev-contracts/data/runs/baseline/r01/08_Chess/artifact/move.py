'''
move.py
Move value object describing one chess move.
Fields:
  from_square / to_square : (row, col) with row 0 = rank 8 (Black's back rank)
  piece_type              : 'P','N','B','R','Q','K' of the moving piece
  color                   : 'w' or 'b' of the moving piece
  captured_type           : type letter of the captured piece (None if none);
                            for en passant this stays None and is_en_passant is True
  promotion               : 'Q','R','B' or 'N' when a pawn promotes
  is_en_passant           : True for an en-passant capture
  castle                  : 'K' (kingside) or 'Q' (queenside) for castling moves
'''
class Move:
    """Represents a chess move from `from_square` to `to_square`."""
    __slots__ = ('from_square', 'to_square', 'piece_type', 'color',
                 'captured_type', 'promotion', 'is_en_passant', 'castle')
    def __init__(self, from_square, to_square, piece_type, color,
                 captured_type=None, promotion=None,
                 is_en_passant=False, castle=None):
        self.from_square = from_square
        self.to_square = to_square
        self.piece_type = piece_type
        self.color = color
        self.captured_type = captured_type
        self.promotion = promotion
        self.is_en_passant = is_en_passant
        self.castle = castle
    @property
    def is_capture(self):
        return self.captured_type is not None or self.is_en_passant
    def __eq__(self, other):
        if not isinstance(other, Move):
            return NotImplemented
        return (self.from_square == other.from_square
                and self.to_square == other.to_square
                and self.promotion == other.promotion
                and self.castle == other.castle)
    def __hash__(self):
        return hash((self.from_square, self.to_square, self.promotion, self.castle))
    def __repr__(self):
        return "Move(%r -> %r, %s%s%s%s)" % (
            self.from_square, self.to_square, self.piece_type,
            'x' if self.is_capture else '',
            '=' + self.promotion if self.promotion else '',
            ' castle=' + self.castle if self.castle else '')