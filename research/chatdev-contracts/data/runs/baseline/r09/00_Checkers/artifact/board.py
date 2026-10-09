'''
board.py
The 8x8 checkers board.
Square (row, col) uses 0-based indices; row 0 is the bottom rank
(notation rank "1") and column 0 is the left-most file (notation
file "a"). Only dark squares are playable; with this orientation a
square is dark when (row + col) is even, so "a1" is a dark corner,
as in standard checkers.
The board owns piece placement and applies validated moves, including
automatic kinging when a man reaches its farthest rank.
'''
from pieces import Piece, PieceColor
BOARD_SIZE = 8
RED_ROWS = range(0, 3)      # notation ranks 1-3
BLACK_ROWS = range(5, 8)    # notation ranks 6-8
class Board:
    """8x8 board holding Piece objects (or None) per square."""
    def __init__(self):
        self.grid = [[None] * BOARD_SIZE for _ in range(BOARD_SIZE)]
        self._setup()
    def _setup(self):
        for row in RED_ROWS:
            for col in range(BOARD_SIZE):
                if self.is_playable(row, col):
                    self.grid[row][col] = Piece(PieceColor.RED)
        for row in BLACK_ROWS:
            for col in range(BOARD_SIZE):
                if self.is_playable(row, col):
                    self.grid[row][col] = Piece(PieceColor.BLACK)
    @staticmethod
    def in_bounds(row, col):
        return 0 <= row < BOARD_SIZE and 0 <= col < BOARD_SIZE
    @staticmethod
    def is_playable(row, col):
        """Dark squares are the playable squares in checkers."""
        return (row + col) % 2 == 0
    def get_piece(self, row, col):
        if not self.in_bounds(row, col):
            return None
        return self.grid[row][col]
    def apply_move(self, move):
        """Apply a validated move; returns True if the move crowned a king."""
        piece = self.grid[move.start_row][move.start_col]
        self.grid[move.start_row][move.start_col] = None
        if move.is_jump:
            self.grid[move.captured[0]][move.captured[1]] = None
        self.grid[move.end_row][move.end_col] = piece
        crowned = False
        if not piece.is_king:
            if (piece.color is PieceColor.RED and move.end_row == BOARD_SIZE - 1) or \
               (piece.color is PieceColor.BLACK and move.end_row == 0):
                piece.crown()
                crowned = True
        return crowned
    def count_pieces(self, color):
        return sum(
            1
            for row in range(BOARD_SIZE)
            for col in range(BOARD_SIZE)
            if self.grid[row][col] is not None and self.grid[row][col].color is color
        )
    def clone(self):
        """Deep copy (new Piece objects) for move simulation."""
        new_board = Board.__new__(Board)
        new_board.grid = [
            [(p.copy() if p is not None else None) for p in row]
            for row in self.grid
        ]
        return new_board