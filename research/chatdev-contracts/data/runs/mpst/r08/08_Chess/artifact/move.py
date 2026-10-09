'''
move.py
Defines the Move class representing a single chess move candidate.
Coordinates are (file, rank) tuples with file 0..7 = a..h and rank 0..7 = 1..8.
'''
class Move:
    def __init__(self, from_sq, to_sq, piece, captured=None, promotion=None, is_en_passant=False):
        self.from_sq = from_sq
        self.to_sq = to_sq
        self.piece = piece
        self.captured = captured
        self.promotion = promotion
        self.is_en_passant = is_en_passant
    @property
    def is_castle(self):
        return isinstance(self.piece, King) and abs(self.to_sq[0] - self.from_sq[0]) == 2
    def san(self):
        """Return a simple SAN string for logging the move."""
        if self.is_castle:
            return 'O-O' if self.to_sq[0] == 6 else 'O-O-O'
        letter = '' if isinstance(self.piece, Pawn) else self.piece.letter
        capture = 'x' if (self.captured is not None or self.is_en_passant) else ''
        dest = chr(ord('a') + self.to_sq[0]) + str(self.to_sq[1] + 1)
        promo = '=' + self.promotion if self.promotion else ''
        return f'{letter}{capture}{dest}{promo}'