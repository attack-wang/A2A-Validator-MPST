'''
board.py
Defines the Board class: the 6x7 Connect Four grid, disc placement,
win/draw detection and text rendering.
'''
from exceptions import ColumnFullError, InvalidColumnError
class Board:
    """A six-row, seven-column Connect Four board."""
    ROWS = 6
    COLS = 7
    EMPTY = '.'
    WIN_LENGTH = 4
    # (row_step, col_step) pairs covering horizontal, vertical and both
    # diagonal winning directions.
    DIRECTIONS = ((0, 1), (1, 0), (1, 1), (1, -1))
    def __init__(self):
        """Initialise an empty grid."""
        self.grid = [[self.EMPTY for _ in range(self.COLS)]
                     for _ in range(self.ROWS)]
    def is_valid_column(self, column):
        """Return True if `column` is an integer within 1..COLS."""
        return isinstance(column, int) and 1 <= column <= self.COLS
    def column_is_full(self, column):
        """Return True if the 1-based `column` has no empty cell left.
        Discs stack from the bottom up, so an occupied top cell means
        the column is full.
        """
        return self.grid[0][column - 1] != self.EMPTY
    def drop_disc(self, column, disc):
        """Drop `disc` into the 1-based `column`.
        The disc occupies the lowest empty cell of the column.
        Returns:
            tuple: (row, col) zero-based grid coordinates of the disc.
        Raises:
            InvalidColumnError: if `column` is outside 1..COLS.
            ColumnFullError: if the column already holds six discs.
        """
        if not self.is_valid_column(column):
            raise InvalidColumnError(
                f"Column must be between 1 and {self.COLS}."
            )
        col_index = column - 1
        for row in range(self.ROWS - 1, -1, -1):
            if self.grid[row][col_index] == self.EMPTY:
                self.grid[row][col_index] = disc
                return row, col_index
        raise ColumnFullError(f"Column {column} is already full.")
    def is_full(self):
        """Return True when every cell is occupied (a draw)."""
        return all(cell != self.EMPTY for row in self.grid for cell in row)
    def check_win(self, row, col, disc):
        """Return True if the disc placed at (row, col) completes a line
        of WIN_LENGTH identical discs horizontally, vertically or
        diagonally."""
        for row_step, col_step in self.DIRECTIONS:
            count = 1  # the disc that was just placed
            count += self._count_direction(row, col, disc, row_step, col_step)
            count += self._count_direction(row, col, disc, -row_step, -col_step)
            if count >= self.WIN_LENGTH:
                return True
        return False
    def _count_direction(self, row, col, disc, row_step, col_step):
        """Count consecutive `disc` cells starting one step away from
        (row, col) and advancing by (row_step, col_step)."""
        count = 0
        r, c = row + row_step, col + col_step
        while 0 <= r < self.ROWS and 0 <= c < self.COLS \
                and self.grid[r][c] == disc:
            count += 1
            r += row_step
            c += col_step
        return count
    def render(self):
        """Return the board as a string with a numbered column header."""
        header = '  ' + ' '.join(str(n) for n in range(1, self.COLS + 1))
        lines = [header]
        lines.extend('  ' + ' '.join(row) for row in self.grid)
        return '\n'.join(lines)