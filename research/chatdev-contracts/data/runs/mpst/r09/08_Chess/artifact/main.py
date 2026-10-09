class Piece:
    def __init__(self, color, symbol):
        self.color = color  # 'w' or 'b'
        self.symbol = symbol  # uppercase letter like 'K', 'Q', etc.
        self.has_moved = False
    def pseudo_moves(self, board, row, col):
        # returns list of (r, c) destination squares
        raise NotImplementedError