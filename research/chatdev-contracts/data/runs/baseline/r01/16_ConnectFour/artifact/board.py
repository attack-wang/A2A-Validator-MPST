'''
board.py
Defines the Board class for the Connect Four game. Handles the grid
state, disc placement with gravity, board rendering, and win/draw
detection logic.
'''
class Board:
    """Represents the Connect Four grid (6 rows x 7 columns)."""
    ROWS = 6
    COLUMNS = 7
    EMPTY = '.'
    WIN_LENGTH = 4
    def __init__(self):
        """Initialize an empty Connect Four grid."""
        self.grid = [[self.EMPTY for _ in range(self.COLUMNS)]
                     for _ in range(self.ROWS)]
    def display(self):
        """Print the current board with column number headers."""
        header = ' '.join(str(col + 1) for col in range(self.COLUMNS))
        print(' ' + header)
        for row in self.grid:
            print('|' + '|'.join(row) + '|')
        print('-' * (self.COLUMNS * 2 + 1))
    def is_valid_column(self, column):
        """Return True if a 0-based column index is in range and not full."""
        if column < 0 or column >= self.COLUMNS:
            return False
        return self.grid[0][column] == self.EMPTY
    def drop_disc(self, column, disc):
        """Place a disc into the column (gravity) and return its row, or None."""
        if not self.is_valid_column(column):
            return None
        for row in range(self.ROWS - 1, -1, -1):
            if self.grid[row][column] == self.EMPTY:
                self.grid[row][column] = disc
                return row
        return None
    def is_full(self):
        """Return True when every cell of the grid is occupied (draw)."""
        return all(cell != self.EMPTY for row in self.grid for cell in row)
    def check_win(self, row, column, disc):
        """Return True if the disc at (row, column) completes a 4-in-a-row."""
        directions = [(0, 1), (1, 0), (1, 1), (1, -1)]
        for d_row, d_col in directions:
            count = 1
            count += self._count_direction(row, column, d_row, d_col, disc)
            count += self._count_direction(row, column, -d_row, -d_col, disc)
            if count >= self.WIN_LENGTH:
                return True
        return False
    def _count_direction(self, row, column, d_row, d_col, disc):
        """Count consecutive matching discs from a cell in one direction."""
        count = 0
        r, c = row + d_row, column + d_col
        while 0 <= r < self.ROWS and 0 <= c < self.COLUMNS \
                and self.grid[r][c] == disc:
            count += 1
            r += d_row
            c += d_col
        return count