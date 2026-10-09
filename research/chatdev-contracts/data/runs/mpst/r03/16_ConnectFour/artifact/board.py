'''
Module: board.py
Defines the Board class for the Connect Four game. The Board manages a
seven-column, six-row grid, handles disc placement with gravity (discs
stack from the bottom up), validates column choices, detects winning
lines (horizontal, vertical, and both diagonals), and renders the grid
to the console.
'''
class Board:
    """Represents the Connect Four grid and its placement/win rules."""
    EMPTY = ' '
    def __init__(self, rows=6, cols=7):
        """Initialize an empty grid with the given number of rows and columns."""
        self.rows = rows
        self.cols = cols
        self.grid = [[self.EMPTY for _ in range(cols)] for _ in range(rows)]
    def is_valid_column(self, col):
        """Return True if col is inside the grid and the column is not full."""
        return 0 <= col < self.cols and self.grid[0][col] == self.EMPTY
    def get_available_row(self, col):
        """Return the lowest empty row index in col, or None if the column is full."""
        for row in range(self.rows - 1, -1, -1):
            if self.grid[row][col] == self.EMPTY:
                return row
        return None
    def drop_disc(self, col, disc):
        """Place disc into col; return the row it landed in, or None if invalid."""
        if not self.is_valid_column(col):
            return None
        row = self.get_available_row(col)
        self.grid[row][col] = disc
        return row
    def check_win(self, row, col, disc):
        """Return True if the disc at (row, col) completes a line of four."""
        return (
            self._count_consecutive(row, col, disc, 0, 1) >= 4 or   # horizontal
            self._count_consecutive(row, col, disc, 1, 0) >= 4 or   # vertical
            self._count_consecutive(row, col, disc, 1, 1) >= 4 or   # diagonal "\"
            self._count_consecutive(row, col, disc, 1, -1) >= 4     # diagonal "/"
        )
    def _count_consecutive(self, row, col, disc, delta_row, delta_col):
        """Count discs matching disc along the line through (row, col) in both directions."""
        count = 1  # the disc just placed
        # Scan in the positive direction.
        r, c = row + delta_row, col + delta_col
        while 0 <= r < self.rows and 0 <= c < self.cols and self.grid[r][c] == disc:
            count += 1
            r += delta_row
            c += delta_col
        # Scan in the negative direction.
        r, c = row - delta_row, col - delta_col
        while 0 <= r < self.rows and 0 <= c < self.cols and self.grid[r][c] == disc:
            count += 1
            r -= delta_row
            c -= delta_col
        return count
    def is_full(self):
        """Return True when every column is full (top row occupied), i.e. a draw."""
        return all(self.grid[0][c] != self.EMPTY for c in range(self.cols))
    def display(self):
        """Print the grid with 1-based column numbers for player reference."""
        header = ' ' + ' '.join(str(c + 1) for c in range(self.cols))
        print(header)
        for row in self.grid:
            print('|' + '|'.join(row) + '|')
        print('+' + '-' * (2 * self.cols - 1) + '+')