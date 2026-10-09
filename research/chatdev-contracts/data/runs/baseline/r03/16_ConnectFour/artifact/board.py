'''
Board module for the Connect Four game.
Defines the Board class, which owns the 6-row by 7-column grid,
implements gravity-based disc placement, win/draw detection, and
console rendering.
'''
from exceptions import ColumnFullError, InvalidColumnError
class Board:
    """Represents the Connect Four grid and enforces its placement rules."""
    ROWS = 6
    COLS = 7
    EMPTY = '.'
    CONNECT = 4
    # (row_delta, col_delta) pairs describing the four axes to scan for a win.
    DIRECTIONS = (
        (0, 1),   # horizontal
        (1, 0),   # vertical
        (1, 1),   # diagonal (top-left to bottom-right)
        (1, -1),  # anti-diagonal (top-right to bottom-left)
    )
    def __init__(self, rows=ROWS, cols=COLS):
        """Create an empty grid of the given dimensions."""
        self.rows = rows
        self.cols = cols
        self.grid = [[self.EMPTY for _ in range(cols)] for _ in range(rows)]
    def reset(self):
        """Clear every cell so a fresh match can start."""
        self.grid = [[self.EMPTY for _ in range(self.cols)] for _ in range(self.rows)]
    def is_valid_column(self, col):
        """Return True if col is an integer index within the grid bounds."""
        return isinstance(col, int) and 0 <= col < self.cols
    def get_next_open_row(self, col):
        """Return the lowest empty row index in the given column.
        Raises:
            InvalidColumnError: if col is outside the grid bounds.
            ColumnFullError: if the column already contains six discs.
        """
        if not self.is_valid_column(col):
            raise InvalidColumnError(
                f"Column {col + 1} is out of range; choose 1-{self.cols}."
            )
        for row in range(self.rows - 1, -1, -1):
            if self.grid[row][col] == self.EMPTY:
                return row
        raise ColumnFullError(f"Column {col + 1} is already full.")
    def drop_disc(self, col, disc):
        """Place a disc into the column and return its (row, col) position."""
        row = self.get_next_open_row(col)
        self.grid[row][col] = disc
        return row, col
    def is_full(self):
        """Return True when the top row is fully occupied (draw condition)."""
        return all(self.grid[0][col] != self.EMPTY for col in range(self.cols))
    def check_win(self, row, col, disc):
        """Return True if the disc at (row, col) completes a line of four.
        Scans outward from the placed disc along each axis (horizontal,
        vertical, and both diagonals), counting consecutive matching discs.
        """
        for dr, dc in self.DIRECTIONS:
            count = 1  # the disc that was just placed
            for sign in (1, -1):
                r, c = row + sign * dr, col + sign * dc
                while (
                    0 <= r < self.rows
                    and 0 <= c < self.cols
                    and self.grid[r][c] == disc
                ):
                    count += 1
                    r += sign * dr
                    c += sign * dc
            if count >= self.CONNECT:
                return True
        return False
    def render(self):
        """Print the grid with numbered columns to the console."""
        header = ' '.join(str(col + 1) for col in range(self.cols))
        separator = '-' * len(header)
        print(header)
        print(separator)
        for row in self.grid:
            print(' '.join(row))
        print(separator)