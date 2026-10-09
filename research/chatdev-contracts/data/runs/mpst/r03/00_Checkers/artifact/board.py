'''
board.py
Board class: 8x8 grid, setup, display, coordinate helpers.
Internal coordinates are (row, col) with row 0 at the TOP of the printed
board and row 7 at the bottom. Red pieces start at the bottom and move
upward (toward row 0); Black pieces start at the top and move downward.
Only dark squares — those where (row + col) % 2 == 1 — are playable.
'''
from pieces import Piece, RED, BLACK
BOARD_SIZE = 8
class Board:
    def __init__(self):
        self.grid = [[None] * BOARD_SIZE for _ in range(BOARD_SIZE)]
        self.setup()
    def setup(self):
        # Black pieces on top three rows (internal rows 0-2), red on bottom (5-7)
        for row in range(BOARD_SIZE):
            for col in range(BOARD_SIZE):
                if self.is_playable(row, col):
                    if row < 3:
                        self.grid[row][col] = Piece(BLACK)
                    elif row > 4:
                        self.grid[row][col] = Piece(RED)
    @staticmethod
    def is_playable(row, col):
        return 0 <= row < BOARD_SIZE and 0 <= col < BOARD_SIZE and (row + col) % 2 == 1
    @staticmethod
    def in_bounds(row, col):
        return 0 <= row < BOARD_SIZE and 0 <= col < BOARD_SIZE
    def get_piece(self, row, col):
        return self.grid[row][col]
    def place_piece(self, piece, row, col):
        self.grid[row][col] = piece
    def remove_piece(self, row, col):
        self.grid[row][col] = None
    def move_piece(self, from_pos, to_pos):
        fr, fc = from_pos
        tr, tc = to_pos
        self.grid[tr][tc] = self.grid[fr][fc]
        self.grid[fr][fc] = None
    def count_pieces(self, color):
        return sum(1 for r in range(BOARD_SIZE) for c in range(BOARD_SIZE)
                   if self.grid[r][c] is not None and self.grid[r][c].color == color)
    def copy(self):
        new = Board.__new__(Board)
        new.grid = []
        for r in range(BOARD_SIZE):
            row = []
            for c in range(BOARD_SIZE):
                p = self.grid[r][c]
                if p is None:
                    row.append(None)
                else:
                    clone = Piece(p.color)
                    if p.is_king:
                        clone.crown()
                    row.append(clone)
            new.grid.append(row)
        return new
    def display(self):
        # print 8 rows with column labels a-h and row numbers 1-8
        lines = []
        header = '   ' + '  '.join(chr(ord('a') + c) for c in range(BOARD_SIZE))
        lines.append(header)
        for r in range(BOARD_SIZE):
            cells = []
            for c in range(BOARD_SIZE):
                p = self.grid[r][c]
                cells.append(p.symbol if p is not None else '.')
            lines.append(f" {8 - r}  " + '  '.join(cells))
        print('\n'.join(lines))