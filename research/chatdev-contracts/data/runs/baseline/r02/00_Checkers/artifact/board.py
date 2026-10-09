'''
board.py
Board representation for the checkers game: an 8x8 grid that knows about
dark (playable) squares, holds Piece objects, and can render itself as text.
'''
from piece import Piece
class Board:
    SIZE = 8
    def __init__(self):
        self.grid = [[None for _ in range(Board.SIZE)] for _ in range(Board.SIZE)]
        self.setup_initial_pieces()
    @staticmethod
    def in_bounds(row, col):
        return 0 <= row < Board.SIZE and 0 <= col < Board.SIZE
    @staticmethod
    def is_dark_square(row, col):
        # a1 (row 7, col 0) is dark -> dark squares satisfy (row + col) % 2 == 1
        return (row + col) % 2 == 1
    def setup_initial_pieces(self):
        for row in range(Board.SIZE):
            for col in range(Board.SIZE):
                if not self.is_dark_square(row, col):
                    continue
                if row <= 2:
                    self.grid[row][col] = Piece(Piece.BLACK)
                elif row >= 5:
                    self.grid[row][col] = Piece(Piece.RED)
    def get_piece(self, row, col):
        if not self.in_bounds(row, col):
            return None
        return self.grid[row][col]
    def place_piece(self, piece, row, col):
        self.grid[row][col] = piece
    def remove_piece(self, row, col):
        piece = self.grid[row][col]
        self.grid[row][col] = None
        return piece
    def move_piece(self, from_row, from_col, to_row, to_col):
        piece = self.remove_piece(from_row, from_col)
        self.place_piece(piece, to_row, to_col)
        return piece
    def count_pieces(self, color):
        return sum(1 for row in range(Board.SIZE) for col in range(Board.SIZE)
                   if self.grid[row][col] is not None and self.grid[row][col].color == color)
    def render(self):
        ...