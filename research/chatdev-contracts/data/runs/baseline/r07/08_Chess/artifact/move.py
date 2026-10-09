'''
Move representation for the chess game.
A Move object stores everything needed to apply, undo, and notate a chess
move: origin and destination squares, special-move flags (castling, en
passant, promotion) and the pieces involved.
'''
class Move:
    """Represents a single chess move."""
    def __init__(self, from_sq, to_sq, piece=None, captured=None,
                 is_en_passant=False, is_castle_king=False,
                 is_castle_queen=False, promotion=None,
                 promotion_needed=False, is_double_push=False):
        self.from_sq = from_sq
        self.to_sq = to_sq
        self.piece = piece
        self.captured = captured
        self.is_en_passant = is_en_passant
        self.is_castle_king = is_castle_king
        self.is_castle_queen = is_castle_queen
        self.promotion = promotion
        self.promotion_needed = promotion_needed
        self.is_double_push = is_double_push
    def is_capture(self):
        return self.captured is not None or self.is_en_passant
    def is_castle(self):
        return self.is_castle_king or self.is_castle_queen
    def __repr__(self):
        return "Move({}{}{})".format(
            square_name(self.from_sq),
            'x' if self.is_capture() else '-',
            square_name(self.to_sq))