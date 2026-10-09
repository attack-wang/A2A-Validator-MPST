class Board:
    def __init__(self):
        self.grid = [[None] * 8 for _ in range(8)]
        self.turn = WHITE
        self.castling_rights = {'K': True, 'Q': True, 'k': True, 'q': True}
        self.en_passant_target = None  # (row, col) of the square that can be captured into
        self.halfmove_clock = 0
        self.fullmove_number = 1
        self.setup()
    def setup(self):
        back = ['R', 'N', 'B', 'Q', 'K', 'B', 'N', 'R']
        for col in range(8):
            self.grid[0][col] = back[col].lower()  # black back rank
            self.grid[1][col] = 'p'
            self.grid[6][col] = 'P'
            self.grid[7][col] = back[col]  # white back rank
        self.turn = WHITE
        self.castling_rights = {'K': True, 'Q': True, 'k': True, 'q': True}
        self.en_passant_target = None