'''
board.py
Board class: 8x8 grid, piece placement, move generation/validation,
capture execution, kinging, and win detection.
'''
from piece import Piece
from exceptions import IllegalMoveError
BOARD_SIZE = 8
class Board:
    def __init__(self):
        self.grid = [[None for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]
        self._setup()
    def _setup(self):
        # Red on ranks 1-3 (rows 0-2), Black on ranks 6-8 (rows 5-7), dark squares only
        for row in range(BOARD_SIZE):
            for col in range(BOARD_SIZE):
                if self.is_dark_square(row, col):
                    if row <= 2:
                        self.grid[row][col] = Piece(Piece.RED)
                    elif row >= 5:
                        self.grid[row][col] = Piece(Piece.BLACK)
    @staticmethod
    def is_dark_square(row, col):
        return (row + col) % 2 == 0
    @staticmethod
    def in_bounds(row, col):
        return 0 <= row < BOARD_SIZE and 0 <= col < BOARD_SIZE
    def get_piece(self, row, col):
        if not self.in_bounds(row, col):
            return None
        return self.grid[row][col]
    def get_all_pieces(self, color):
        pieces = []
        for row in range(BOARD_SIZE):
            for col in range(BOARD_SIZE):
                piece = self.grid[row][col]
                if piece is not None and piece.color == color:
                    pieces.append(((row, col), piece))
        return pieces