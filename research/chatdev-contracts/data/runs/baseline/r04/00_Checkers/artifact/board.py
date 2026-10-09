'''
board.py
Board representation for the checkers game.
The board is an 8x8 grid. Only the dark squares are playable; with the
convention used here (row 0 is the top rank "8", column 0 is file "a")
a square is dark when (row + column) % 2 == 1, which places a dark
square on a1 as required by the standard starting position.
The Board class owns the grid, sets up the standard starting position,
renders an ASCII picture of the board with coordinates, and provides
low-level helpers (bounds checks, piece placement/removal, crowning).
'''
from piece import Piece, PieceColor
BOARD_SIZE = 8
RED_KING_ROW = 0
BLACK_KING_ROW = BOARD_SIZE - 1
class Board:
    """The 8x8 checkers board with its pieces."""
    def __init__(self):
        self._grid = [[None for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]
        self._setup_starting_position()
    def _setup_starting_position(self):
        """Place 12 black men on rows 0-2 and 12 red men on rows 5-7."""
        for row in range(BOARD_SIZE):
            for col in range(BOARD_SIZE):
                if not self.is_dark(row, col):
                    continue
                if row <= 2:
                    self._grid[row][col] = Piece(PieceColor.BLACK)
                elif row >= 5:
                    self._grid[row][col] = Piece(PieceColor.RED)
    @staticmethod
    def is_dark(row, col):
        """True when (row, col) is a playable dark square."""
        return (row + col) % 2 == 1
    @staticmethod
    def in_bounds(row, col):
        """True when (row, col) lies on the board."""
        return 0 <= row < BOARD_SIZE and 0 <= col < BOARD_SIZE
    def is_empty(self, row, col):
        """True when the square is on the board and holds no piece."""
        return self.in_bounds(row, col) and self._grid[row][col] is None
    def get_piece(self, row, col):
        """Return the piece at (row, col), or None if empty/out of bounds."""
        if not self.in_bounds(row, col):
            return None
        return self._grid[row][col]
    def place_piece(self, piece, row, col):
        """Put a piece on a square (overwriting whatever was there)."""
        self._grid[row][col] = piece
    def remove_piece(self, row, col):
        """Take the piece off a square and return it (or None)."""
        piece = self._grid[row][col]
        self._grid[row][col] = None
        return piece
    @staticmethod
    def king_row(color):
        """The row a man of `color` must reach to be crowned."""
        return RED_KING_ROW if color is PieceColor.RED else BLACK_KING_ROW
    def count_pieces(self, color):
        """How many pieces of `color` remain on the board."""
        return sum(
            1
            for row in range(BOARD_SIZE)
            for col in range(BOARD_SIZE)
            if self._grid[row][col] is not None
            and self._grid[row][col].color is color
        )
    def render(self):
        """Return an ASCII picture of the board with coordinates."""
        lines = []
        lines.append("    a   b   c   d   e   f   g   h")
        lines.append("  +---+---+---+---+---+---+---+---+")
        for row in range(BOARD_SIZE):
            cells = []
            for col in range(BOARD_SIZE):
                piece = self._grid[row][col]
                if piece is None:
                    ch = "." if self.is_dark(row, col) else " "
                else:
                    ch = piece.symbol
                cells.append(f" {ch} ")
            rank = BOARD_SIZE - row
            lines.append(f"{rank} |" + "|".join(cells) + "|")
            lines.append("  +---+---+---+---+---+---+---+---+")
        return "\n".join(lines)