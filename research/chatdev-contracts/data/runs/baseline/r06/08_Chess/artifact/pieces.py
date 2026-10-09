'''Chess piece classes with movement generation.'''
from move import Move
WHITE = 'w'
BLACK = 'b'
KNIGHT_OFFSETS = [(...)]
KING_OFFSETS = [...]
ROOK_DIRS = [...]
BISHOP_DIRS = [...]
def in_bounds(r, c): return 0 <= r < 8 and 0 <= c < 8
class Piece:
    letter = '?'
    value = 0
    def __init__(self, color):
        self.color = color
    @property
    def symbol(self):
        return self.letter.upper() if self.color == WHITE else self.letter.lower()
    def pseudo_legal_moves(self, board, r, c):
        raise NotImplementedError
class Pawn(Piece):
    letter = 'p'
    value = 1
    def pseudo_legal_moves(self, board, r, c):
        moves = []
        direction = -1 if self.color == WHITE else 1
        start_row = 6 if self.color == WHITE else 1
        promo_row = 0 if self.color == WHITE else 7
        # forward one
        r1 = r + direction
        if in_bounds(r1, c) and board.get(r1, c) is None:
            if r1 == promo_row:
                for p in ('Q','R','B','N'):
                    moves.append(Move((r,c),(r1,c),self,promotion=p))
            else:
                moves.append(Move((r,c),(r1,c),self))
            # forward two
            r2 = r + 2*direction
            if r == start_row and board.get(r2, c) is None:
                moves.append(Move((r,c),(r2,c),self,is_double_push=True))
        # captures
        for dc in (-1, 1):
            c1 = c + dc
            r1 = r + direction
            if in_bounds(r1, c1):
                target = board.get(r1, c1)
                if target is not None and target.color != self.color:
                    if r1 == promo_row:
                        for p in ('Q','R','B','N'):
                            moves.append(Move((r,c),(r1,c1),self,captured=target,promotion=p))
                    else:
                        moves.append(Move((r,c),(r1,c1),self,captured=target))
                elif target is None and (r1, c1) == board.en_passant_target:
                    # en passant: captured pawn is at (r, c1)
                    captured = board.get(r, c1)
                    if captured is not None and isinstance(captured, Pawn) and captured.color != self.color:
                        moves.append(Move((r,c),(r1,c1),self,captured=captured,is_en_passant=True))
        return moves