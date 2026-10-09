class Piece:
    def __init__(self, color):
        self.color = color  # 'w' or 'b'
    @property
    def symbol(self): ...
    def pseudo_legal_moves(self, board, row, col): return []