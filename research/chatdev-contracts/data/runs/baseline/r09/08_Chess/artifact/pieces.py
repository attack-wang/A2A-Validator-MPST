'''
pieces.py
Defines the Piece class hierarchy (Pawn, Knight, Bishop, Rook, Queen, King)
and the Move record used by the chess engine.
'''
class Piece:
    LETTER = '?'
    VALUE = 0
    def __init__(self, color):
        self.color = color  # 'w' or 'b'
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
        # helper to append moves, expanding promotions for pawns
        ...
class Pawn(Piece):
    LETTER = 'P'
    def pseudo_moves(self, board, file, rank):
        ...