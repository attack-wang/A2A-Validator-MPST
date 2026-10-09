'''
board.py
This module defines the Board class, which represents the Connect Four grid.
It manages disc placement, column validation, and win/draw detection logic.
'''
class Board:
    """Represents the Connect Four game board (6 rows x 7 columns)."""
    ROWS = 6
    COLS = 7
    WIN_LENGTH = 4
    EMPTY = '.'
    # The four directions to scan for a winning line:
    # horizontal, vertical, diagonal down-right, diagonal up-right.
    DIRECTIONS = [(0, 1), (1, 0), (1, 1), (1, -1)]
    def __init__(self, rows=ROWS, cols=COLS):
        """Initialize an empty board with the given dimensions."""
        self.rows = rows
        self.cols = cols
        self.grid = [[self.EMPTY for _ in range(cols)] for _ in range(rows)]
    def is_valid_column(self, col):
        """Return True if col is within bounds and not full."""
        return 0 <= col < self.cols and self.grid[0][col] == self.EMPTY
    def drop_disc(self, col, disc):
        """
        Place a disc into the given column (0-indexed).
        Returns the row index where the disc landed, or None if invalid.
        """
        if not self.is_valid_column(col):
            return None
        for row in range(self.rows - 1, -1, -1):
            if self.grid[row][col] == self.EMPTY:
                self.grid[row][col] = disc
                return row
        return None
    def is_full(self):
        """Return True if every cell is occupied (draw condition)."""
        return all(self.grid[0][col] != self.EMPTY for col in range(self.cols))
    def check_win(self, row, col, disc):
        """
        Check whether the disc just placed at (row, col) completes a line
        of WIN_LENGTH identical discs in any direction.
        """
        for dr, dc in self.DIRECTIONS:
            count = 1  # the disc just placed
            count += self._count_direction(row, col, dr, dc, disc)
            count += self._count_direction(row, col, -dr, -dc, disc)
            if count >= self.WIN_LENGTH:
                return True
        return False
    def _count_direction(self, row, col, dr, dc, disc):
        """Count consecutive discs matching `disc` starting from (row, col)
        moving in direction (dr, dc)."""
        count = 0
        r, c = row + dr, col + dc
        while 0 <= r < self.rows and 0 <= c < self.cols and self.grid[r][c] == disc:
            count += 1
            r += dr
            c += dc
        return count
    def get_available_columns(self):
        """Return a list of 0-indexed columns that can still accept a disc."""
        return [col for col in range(self.cols) if self.is_valid_column(col)]