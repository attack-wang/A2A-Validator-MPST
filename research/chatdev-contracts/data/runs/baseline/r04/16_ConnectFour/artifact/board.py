'''
board.py
Implements the Connect Four grid: a six-row, seven-column board into
which discs fall under gravity to the lowest empty cell. The Board owns
the grid state, disc placement, full-board detection, win detection
(horizontal, vertical and both diagonals) and pretty-printing of the
current position.
'''
from exceptions import ColumnFullError, InvalidColumnError
class Board:
    """Seven-column, six-row grid with gravity-based disc placement."""
    ROWS = 6
    COLUMNS = 7
    WIN_LENGTH = 4
    EMPTY = '.'
    # (delta_row, delta_col) steps for the four line orientations that can
    # hold a win: horizontal, vertical, diagonal '\' and diagonal '/'.
    DIRECTIONS = ((0, 1), (1, 0), (1, 1), (1, -1))
    def __init__(self, rows=ROWS, columns=COLUMNS):
        """Create an empty grid stored as row lists (row 0 is the top row)."""
        self._rows = rows
        self._columns = columns
        self._grid = [[self.EMPTY for _ in range(columns)] for _ in range(rows)]
    @property
    def rows(self):
        """Number of rows in the grid."""
        return self._rows
    @property
    def columns(self):
        """Number of columns in the grid."""
        return self._columns
    def is_valid_column(self, column):
        """
        Validate a 1-based column choice.
        Returns:
            bool: True when the column is in range and still has space.
        Raises:
            InvalidColumnError: If column is not an int within 1..COLUMNS.
            ColumnFullError: If the column has no empty cell left.
        """
        if not isinstance(column, int) or not 1 <= column <= self._columns:
            raise InvalidColumnError(column)
        if self._grid[0][column - 1] != self.EMPTY:
            raise ColumnFullError(column)
        return True
    def drop_disc(self, column, disc):
        """
        Drop `disc` into `column`; it lands in the lowest empty row.
        Args:
            column (int): 1-based column index chosen by the player.
            disc (str): Symbol to place, e.g. 'X' or 'O'.
        Returns:
            tuple[int, int]: 0-based (row, col) where the disc landed.
        Raises:
            InvalidColumnError / ColumnFullError: via is_valid_column().
        """
        self.is_valid_column(column)
        col_index = column - 1
        for row_index in range(self._rows - 1, -1, -1):
            if self._grid[row_index][col_index] == self.EMPTY:
                self._grid[row_index][col_index] = disc
                return row_index, col_index
        raise ColumnFullError(column)  # Defensive; validation above prevents this.
    def is_full(self):
        """Return True when every top-row cell is occupied (draw condition)."""
        return all(cell != self.EMPTY for cell in self._grid[0])
    def check_win(self, row, col, disc):
        """
        Report whether the disc just placed at (row, col) completes a line
        of at least WIN_LENGTH identical discs in any direction.
        Args:
            row (int): 0-based row where the last disc landed.
            col (int): 0-based column where the last disc landed.
            disc (str): Symbol of the player who just moved.
        Returns:
            bool: True if the move wins the game.
        """
        for delta_row, delta_col in self.DIRECTIONS:
            count = 1  # The disc that was just placed.
            count += self._count_direction(row, col, disc, delta_row, delta_col)
            count += self._count_direction(row, col, disc, -delta_row, -delta_col)
            if count >= self.WIN_LENGTH:
                return True
        return False
    def _count_direction(self, row, col, disc, delta_row, delta_col):
        """Count consecutive `disc` cells extending from (row, col) one way."""
        count = 0
        current_row, current_col = row + delta_row, col + delta_col
        while 0 <= current_row < self._rows and 0 <= current_col < self._columns:
            if self._grid[current_row][current_col] != disc:
                break
            count += 1
            current_row += delta_row
            current_col += delta_col
        return count
    def display(self):
        """Print the grid with 1-based column numbers underneath it."""
        print()
        for row in self._grid:
            print(' ' + ' '.join(row))
        print(' ' + ' '.join(str(number) for number in range(1, self._columns + 1)))
        print()