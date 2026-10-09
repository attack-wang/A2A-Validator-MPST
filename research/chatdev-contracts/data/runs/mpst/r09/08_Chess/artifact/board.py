class Board:
    def __init__(self):
        self.grid = [[None]*8 for _ in range(8)]
        self.setup()
    def setup(self):
        back = [Rook, Knight, Bishop, Queen, King, Bishop, Knight, Rook]
        for col in range(8):
            self.grid[0][col] = back[col]('b')  # rank 8
            self.grid[1][col] = Pawn('b')
            self.grid[6][col] = Pawn('w')
            self.grid[7][col] = back[col]('w')  # rank 1
    def copy(self):
        # deep copy of pieces
        new = Board.__new__(Board)
        new.grid = [[None]*8 for _ in range(8)]
        for r in range(8):
            for c in range(8):
                p = self.grid[r][c]
                if p is not None:
                    q = p.clone()  # copy with has_moved
                    new.grid[r][c] = q
        return new
    def find_king(self, color):
        for r in range(8):
            for c in range(8):
                p = self.grid[r][c]
                if p and p.color == color and p.symbol == 'K':
                    return (r, c)
        return None
    def is_attacked(self, row, col, by_color):
        # check if square (row, col) is attacked by by_color
        # pawns, knights, king, sliders
        ...
    def __str__(self):
        # render with +---+ grid