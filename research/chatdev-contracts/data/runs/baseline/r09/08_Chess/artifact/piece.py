class Piece:
    LETTER = '?'
    def __init__(self, color):
        self.color = color
        self.has_moved = False
    @property
    def symbol(self):
        return self.LETTER if self.color == 'w' else self.LETTER.lower()
    @property
    def letter(self):
        return self.LETTER
    def pseudo_moves(self, board, file, rank):
        raise NotImplementedError
    def _add(self, moves, board, from_sq, to_sq, captured=None, flag=None):
        """Append a move; expand into promotion moves when a pawn reaches last rank."""
        if isinstance(self, Pawn) and to_sq[1] == (7 if self.color == 'w' else 0):
            for cls in (Queen, Rook, Bishop, Knight):
                moves.append(Move(from_sq, to_sq, self, captured=captured, promotion=cls, flag=flag))
        else:
            moves.append(Move(from_sq, to_sq, self, captured=captured, flag=flag))