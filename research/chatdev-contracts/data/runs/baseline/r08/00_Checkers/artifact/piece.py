class Piece:
    def __init__(self, color):
        self.color = color  # 'R' or 'B'
        self.king = False
    def crown(self):
        self.king = True
    @property
    def is_king(self):
        return self.king
    def get_symbol(self):
        if self.color == 'R':
            return 'R' if self.king else 'r'
        else:
            return 'B' if self.king else 'b'
    def get_directions(self):
        if self.king:
            return [(-1, -1), (-1, 1), (1, -1), (1, 1)]
        if self.color == 'R':
            return [(-1, -1), (-1, 1)]
        else:
            return [(1, -1), (1, 1)]
    def directions(self):
        # alias for get_directions
        return self.get_directions()