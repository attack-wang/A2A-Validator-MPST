'''
Board class: 8x8 grid, initial setup, piece placement and display.
'''
from constants import (BOARD_SIZE, DARK_SQUARE, LIGHT_SQUARE, RED, BLACK)
from piece import Piece
class Board:
    """The 8x8 checkers board and the pieces standing on it."""
    def __init__(self):
        self.grid = [[None] * BOARD_SIZE for _ in range(BOARD_SIZE)]
        self.setup()
    @staticmethod
    def is_dark(row, col):
        """True for playable (dark) squares; a1 and h8 are dark."""
        return (row + col) % 2 == 1
    def setup(self):
        """Place the 12 red men on ranks 1-3 and the 12 black men on ranks 6-8."""
        for row in range(BOARD_SIZE):
            for col in range(BOARD_SIZE):
                if not self.is_dark(row, col):
                    continue
                if row <= 2:
                    self.grid[row][col] = Piece(BLACK)
                elif row >= 5:
                    self.grid[row][col] = Piece(RED)
    def in_bounds(self, row, col):
        return 0 <= row < BOARD_SIZE and 0 <= col < BOARD_SIZE
    def get_piece(self, row, col):
        return self.grid[row][col]
    def place_piece(self, piece, row, col):
        self.grid[row][col] = piece
    def remove_piece(self, row, col):
        self.grid[row][col] = None
    def move_piece(self, from_pos, to_pos):
        """Move the piece from from_pos to to_pos and return it."""
        piece = self.get_piece(*from_pos)
        self.remove_piece(*from_pos)
        self.place_piece(piece, *to_pos)
        return piece
    def display(self):
        """Return the board as a multi-line string (rank 8 on top)."""
        lines = ["    a b c d e f g h"]
        for row in range(BOARD_SIZE):
            rank = BOARD_SIZE - row
            cells = []
            for col in range(BOARD_SIZE):
                piece = self.grid[row][col]
                if piece is not None:
                    cells.append(piece.symbol)
                elif self.is_dark(row, col):
                    cells.append(DARK_SQUARE)
                else:
                    cells.append(LIGHT_SQUARE)
            lines.append(f" {rank}  " + " ".join(cells))
        return "\n".join(lines)
    def count_pieces(self, color):
        """Number of pieces of the given color still on the board."""
        return sum(
            1
            for row in self.grid
            for cell in row
            if cell is not None and cell.color == color
        )