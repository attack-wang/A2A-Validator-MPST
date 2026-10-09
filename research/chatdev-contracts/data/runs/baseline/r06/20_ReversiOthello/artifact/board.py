'''
board.py
Board state and Reversi (Othello) rules.
The Board class owns the 8x8 grid and implements the core game rules:
legal-move detection, disc flipping along all eight directions, and
score counting.  It is completely independent of the GUI, so the
rules can be tested and reused on their own.
'''
class Board:
    """8x8 Reversi board with the standard starting position."""
    BOARD_SIZE = 8
    EMPTY = 0
    BLACK = 1
    WHITE = 2
    # All eight directions as (row_delta, col_delta).
    DIRECTIONS = [
        (-1, -1), (-1, 0), (-1, 1),
        (0, -1),           (0, 1),
        (1, -1),  (1, 0),  (1, 1),
    ]
    def __init__(self):
        """Create the grid and place the four standard starting discs."""
        self.grid = [
            [self.EMPTY for _ in range(self.BOARD_SIZE)]
            for _ in range(self.BOARD_SIZE)
        ]
        mid = self.BOARD_SIZE // 2
        self.grid[mid - 1][mid - 1] = self.WHITE
        self.grid[mid][mid] = self.WHITE
        self.grid[mid - 1][mid] = self.BLACK
        self.grid[mid][mid - 1] = self.BLACK
    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------
    def in_bounds(self, row, col):
        """Return True if (row, col) lies on the board."""
        return 0 <= row < self.BOARD_SIZE and 0 <= col < self.BOARD_SIZE
    def get_disc(self, row, col):
        """Return the cell state at (row, col): EMPTY, BLACK or WHITE."""
        return self.grid[row][col]
    def _flips_in_direction(self, row, col, dr, dc, color):
        """
        Return the opponent discs that would be captured by placing
        `color` on (row, col) along direction (dr, dc).
        A capture requires a contiguous run of opponent discs ending in
        a friendly disc.  Returns an empty list when the line is not
        closed (edge of board, empty cell, or friendly disc too early).
        """
        opponent = self.WHITE if color == self.BLACK else self.BLACK
        flips = []
        r, c = row + dr, col + dc
        while self.in_bounds(r, c) and self.grid[r][c] == opponent:
            flips.append((r, c))
            r += dr
            c += dc
        if flips and self.in_bounds(r, c) and self.grid[r][c] == color:
            return flips
        return []
    # ------------------------------------------------------------------
    # Rule queries
    # ------------------------------------------------------------------
    def is_valid_move(self, row, col, color):
        """A move is legal only on an empty cell that flips >= 1 disc."""
        if not self.in_bounds(row, col) or self.grid[row][col] != self.EMPTY:
            return False
        return any(
            self._flips_in_direction(row, col, dr, dc, color)
            for dr, dc in self.DIRECTIONS
        )
    def get_valid_moves(self, color):
        """Return a list of all legal (row, col) moves for `color`."""
        return [
            (r, c)
            for r in range(self.BOARD_SIZE)
            for c in range(self.BOARD_SIZE)
            if self.is_valid_move(r, c, color)
        ]
    # ------------------------------------------------------------------
    # Mutations
    # ------------------------------------------------------------------
    def place_disc(self, row, col, color):
        """
        Place a disc on (row, col), flip every captured line and return
        the list of flipped (row, col) cells.
        """
        flipped = []
        for dr, dc in self.DIRECTIONS:
            flipped.extend(self._flips_in_direction(row, col, dr, dc, color))
        self.grid[row][col] = color
        for r, c in flipped:
            self.grid[r][c] = color
        return flipped
    # ------------------------------------------------------------------
    # State queries
    # ------------------------------------------------------------------
    def is_full(self):
        """Return True when no empty cells remain."""
        return all(
            cell != self.EMPTY
            for row in self.grid
            for cell in row
        )
    def count_discs(self):
        """Return the current score as a tuple (black_count, white_count)."""
        black = sum(row.count(self.BLACK) for row in self.grid)
        white = sum(row.count(self.WHITE) for row in self.grid)
        return black, white