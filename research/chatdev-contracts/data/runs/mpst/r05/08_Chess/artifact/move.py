'''
move.py
Defines the Move record used to describe a single chess move, including
the special moves (castling, en passant, promotion) and the SAN string
assigned after the move is played.
'''
class Move:
    """A single chess move.
    Attributes:
        start:      (row, col) of the moving piece.
        end:        (row, col) of the destination square.
        piece:      the Piece object being moved.
        captured:   the Piece object captured, if any (for en passant this is
                    the pawn actually removed, which is NOT on `end`).
        captured_square: (row, col) where the captured piece sits
                    (differs from `end` only for en passant).
        promotion:  letter ('Q', 'R', 'B', 'N') if this is a promotion.
        is_castle:  None, 'K' (kingside) or 'Q' (queenside).
        is_en_passant: True if this move captures en passant.
        san:        the Standard Algebraic Notation string, filled in when
                    the move is applied.
    """
    def __init__(self, start, end, piece, captured=None, captured_square=None,
                 promotion=None, is_castle=None, is_en_passant=False):
        self.start = start
        self.end = end
        self.piece = piece
        self.captured = captured
        self.captured_square = captured_square if captured_square is not None else end
        self.promotion = promotion
        self.is_castle = is_castle
        self.is_en_passant = is_en_passant
        self.san = ''
    def __repr__(self):
        return f"<Move {self.san or (str(self.start) + '->' + str(self.end))}>"