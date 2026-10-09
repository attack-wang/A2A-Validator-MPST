'''
board.py
Defines the Board class: an 8x8 checkers board that stores pieces,
provides setup, queries, mutation, and a console rendering.
'''
from pieces import Piece, PieceColor
BOARD_SIZE = 8
class Board:
    def __init__(self):
        self.grid = [[None for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]
        self.setup()
    def setup(self):
        # Red on rows 0-2 (bottom), Black on rows 5-7 (top), dark squares only.
        for row in range(3):
            for col in range(BOARD_SIZE):
                if self.is_dark_square(row, col):
                    self.grid[row][col] = Piece(PieceColor.RED)
        for row in range(5, 8):
            for col in range(BOARD_SIZE):
                if self.is_dark_square(row, col):
                    self.grid[row][col] = Piece(PieceColor.BLACK)
    @staticmethod
    def is_valid_square(row, col):
        return 0 <= row < BOARD_SIZE and 0 <= col < BOARD_SIZE
    @staticmethod
    def is_dark_square(row, col):
        return (row + col) % 2 == 0
    @staticmethod
    def is_king_row(color, row):
        '''Return True if `row` is the crowning row for `color`.
        Red advances toward grid row 7 (displayed row 8); Black toward row 0.'''
        return row == BOARD_SIZE - 1 if color == PieceColor.RED else row == 0
    def get_piece(self, row, col):
        if not self.is_valid_square(row, col):
            return None
        return self.grid[row][col]
    def place_piece(self, row, col, piece):
        self.grid[row][col] = piece
    def remove_piece(self, row, col):
        self.grid[row][col] = None
    def move_piece(self, from_row, from_col, to_row, to_col):
        piece = self.grid[from_row][from_col]
        self.grid[from_row][from_col] = None
        self.grid[to_row][to_col] = piece
    def count_pieces(self, color):
        '''Count pieces of the given color currently on the board.'''
        return sum(
            1
            for row in self.grid
            for piece in row
            if piece is not None and piece.color == color
        )
    def display(self):
        '''Print the board with grid row 7 shown as row 8 at the top and
        columns labelled a-h, matching the coordinate system used by the
        move parser.'''
        header = "   " + " ".join(chr(ord('a') + c) for c in range(BOARD_SIZE))
        print(header)
        for row in range(BOARD_SIZE - 1, -1, -1):
            cells = []
            for col in range(BOARD_SIZE):
                piece = self.grid[row][col]
                cells.append(piece.symbol if piece else '.')
            print(f" {row + 1} " + " ".join(cells))
        print(header)