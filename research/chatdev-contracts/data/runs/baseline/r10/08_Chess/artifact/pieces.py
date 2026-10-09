class Piece:
    def __init__(self, color):
        self.color = color  # 'w' or 'b'
        self.has_moved = False
    @property
    def symbol(self):
        raise NotImplementedError
    def pseudo_moves(self, board, file, rank):
        # returns list of (file, rank) target squares
        raise NotImplementedError