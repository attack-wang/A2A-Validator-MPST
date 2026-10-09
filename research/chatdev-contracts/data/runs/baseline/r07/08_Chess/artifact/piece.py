# pieces.py
class Piece:
    def __init__(self, color):
        self.color = color
    @property
    def letter(self):
        return ''
    @property
    def value(self):
        return 0
    def unicode_symbol(self):
        raise NotImplementedError
    def ascii_symbol(self):
        raise NotImplementedError
    def pseudo_legal_moves(self, board, row, col, game):
        return []