'''
board.py
Defines the Board class for the Connect Four game. The Board manages the
six-row by seven-column grid, handles disc placement, validates columns,
detects winning lines (horizontal, vertical, and diagonal), checks for a
full grid (draw), and renders the board as text.
'''
from exceptions import ColumnFullError, InvalidColumnError
class Board:
    """Represents the Connect Four grid and its game logic."""
    ROWS = 6
    COLS = 7
    EMPTY = '.'
    WIN_LENGTH = 4
    # Directions used for win detection: horizontal, vertical, two diagonals.
    _DIRECTIONS = ((0, 1), (1, 0), (1, 1), (1, -1))
    def __init__(self, rows=ROWS, cols=COLS):
        """Initialize an empty grid with the given number of rows and columns."""
        self._rows = rows
        self._cols = cols
        self._grid = [[Board.EMPTY for _ in range(cols)] for _ in range(rows)]
    @property
    def rows(self):
        """Return the number of rows in the grid."""
        return self._rows
    @property
    def cols(self):
        """Return the number of columns in the grid."""
        return self._cols
    def is_valid_column(self, col):
        """Return True if the column index is in range and the column is not full."""
        if col < 0 or col >= self._cols:
            return False
        return self._grid[0][col] == Board.EMPTY
    def drop_disc(self, col, disc):
        """Drop a disc into the given column and return the row it landed in.
        Raises InvalidColumnError if the column index is out of range and
        ColumnFullError if the column has no empty cells left.
        """
        if col < 0 or col >= self._cols:
            raise InvalidColumnError(
                "Column {} is out of range (valid: 1-{}).".format(col + 1, self._cols)
            )
        if self._grid[0][col] != Board.EMPTY:
            raise ColumnFullError("Column {} is already full.".format(col + 1))
        for row in range(self._rows - 1, -1, -1):
            if self._grid[row][col] == Board.EMPTY:
                self._grid[row][col] = disc
                return row
        raise ColumnFullError("Column {} is already full.".format(col + 1))
    def check_win(self, row, col, disc):
        """Return True if the disc at (row, col) completes a line of four."""
        for delta_row, delta_col in Board._DIRECTIONS:
            total = (
                1
                + self._count_discs(row, col, disc, delta_row, delta_col)
                + self._count_discs(row, col, disc, -delta_row, -delta_col)
            )
            if total >= Board.WIN_LENGTH:
                return True
        return False
    def is_full(self):
        """Return True when every column is full, meaning the game is a draw."""
        return all(
            self._grid[0][col] != Board.EMPTY for col in range(self._cols)
        )
    def render(self):
        """Return a text rendering of the board with numbered columns."""
        lines = []
        header = ' '.join(str(number) for number in range(1, self._cols + 1))
        lines.append('  ' + header)
        lines.append('  ' + '-' * len(header))
        for row_cells in self._grid:
            lines.append('  ' + ' '.join(row_cells))
        return '\n'.join(lines)
    def _count_discs(self, row, col, disc, delta_row, delta_col):
        """Count consecutive discs matching `disc` starting from (row, col)."""
        count = 0
        current_row = row + delta_row
        current_col = col + delta_col
        while (
            0 <= current_row < self._rows
            and 0 <= current_col < self._cols
            and self._grid[current_row][current_col] == disc
        ):
            count += 1
            current_row += delta_row
            current_col += delta_col
        return count