'''
board.py
The Board class owns the 8x8 piece grid, initial setup, rendering and
low-level piece manipulation (move, capture, place, remove, copy).
It contains no rule logic; rules live in game.py.
'''
from piece import Piece, PieceColor
from constants import BOARD_SIZE, in_bounds, is_playable, FILES
class Board:
    """The 8x8 checkers board and the pieces standing on it."""
    def __init__(self):
        """Create an empty grid and place the 24 starting pieces."""
        self.grid = [[None] * BOARD_SIZE for _ in range(BOARD_SIZE)]
        self.setup()
    def setup(self):
        """Black pieces on the top three playable rows, Red on the bottom three."""
        for row in range(BOARD_SIZE):
            for col in range(BOARD_SIZE):
                if not is_playable(row, col):
                    continue
                if row <= 2:
                    self.grid[row][col] = Piece(PieceColor.BLACK)
                elif row >= 5:
                    self.grid[row][col] = Piece(PieceColor.RED)
    def get_piece(self, row, col):
        """Return the piece at (row, col), or None if empty/out of bounds."""
        if not in_bounds(row, col):
            return None
        return self.grid[row][col]
    def place_piece(self, piece, row, col):
        """Place a piece on (row, col), overwriting whatever was there."""
        if not in_bounds(row, col):
            raise ValueError(f"({row}, {col}) is outside the board")
        self.grid[row][col] = piece
    def remove_piece(self, row, col):
        """Remove and return the piece at (row, col) (None if the square is empty)."""
        piece = self.grid[row][col]
        self.grid[row][col] = None
        return piece
    def move_piece(self, src, dst):
        """Move a piece from src to dst (no capture handling here)."""
        piece = self.grid[src[0]][src[1]]
        self.grid[src[0]][src[1]] = None
        self.grid[dst[0]][dst[1]] = piece
    def capture_piece(self, row, col):
        """Remove and return the captured piece."""
        piece = self.grid[row][col]
        self.grid[row][col] = None
        return piece
    def count_pieces(self, color):
        """Count how many pieces of the given color remain on the board."""
        return sum(1 for r in range(BOARD_SIZE) for c in range(BOARD_SIZE)
                   if self.grid[r][c] and self.grid[r][c].color is color)
    def copy(self):
        """Return a deep copy of the board (independent pieces)."""
        new = Board.__new__(Board)
        new.grid = [[(p.copy() if p else None) for p in row] for row in self.grid]
        return new
    def display(self):
        """Print the board with file/rank labels; '.' = empty playable square."""
        header = "   " + " ".join(FILES)
        print(header)
        for row in range(BOARD_SIZE):
            rank = BOARD_SIZE - row
            cells = []
            for col in range(BOARD_SIZE):
                piece = self.grid[row][col]
                if piece:
                    cells.append(piece.symbol)
                elif is_playable(row, col):
                    cells.append(".")
                else:
                    cells.append(" ")
            print(f" {rank} " + " ".join(cells) + f" {rank}")
        print("   " + " ".join(FILES))