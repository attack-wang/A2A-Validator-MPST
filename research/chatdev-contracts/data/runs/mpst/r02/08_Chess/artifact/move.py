'''Move representation for the chess game.'''
class Move:
    def __init__(self, from_sq, to_sq, piece, captured=None,
                 is_en_passant=False, promotion=None, castle=''):
        self.from_sq = from_sq
        self.to_sq = to_sq
        self.piece = piece
        self.captured = captured
        self.is_en_passant = is_en_passant
        self.promotion = promotion
        self.castle = castle
    def __eq__(self, other):
        if not isinstance(other, Move):
            return NotImplemented
        return (self.from_sq == other.from_sq and
                self.to_sq == other.to_sq and
                self.piece is other.piece and
                self.promotion == other.promotion and
                self.castle == other.castle and
                self.is_en_passant == other.is_en_passant)
    def __repr__(self):
        fr = chr(ord('a') + self.from_sq[1]) + str(8 - self.from_sq[0])
        to = chr(ord('a') + self.to_sq[1]) + str(8 - self.to_sq[0])
        promo = '=' + self.promotion if self.promotion else ''
        castle = ' (castle)' if self.castle else ''
        return f"<Move {self.piece.symbol} {fr}->{to}{promo}{castle}>"