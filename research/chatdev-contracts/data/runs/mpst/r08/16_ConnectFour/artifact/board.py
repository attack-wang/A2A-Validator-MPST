'''
board.py
Defines the Board class for the Connect Four game.
The Board encapsulates the 6-row by 7-column grid, provides disc
placement with gravity (discs stack from the bottom), validates
column choices, renders the grid to the console with column numbers
aligned exactly above their columns, and detects winning lines
(horizontal, vertical, or diagonal) as well as the draw condition
(full grid).
'''
ROWS = 6
COLS = 7
CONNECT = 4
EMPTY = ' '
class Board:
    """Represents the Connect Four grid and its placement/detection rules."""
    def __init__(self, rows=ROWS, cols=COLS):
        """Initialize an empty grid with the given dimensions."""
        self.rows = rows
        self.cols = cols
        self.grid = [[EMPTY for _ in range(cols)] for _ in range(rows)]
    def is_valid_column(self, column):
        """Return True if `column` is an in-range index whose top cell is empty."""
        if not isinstance(column, int) or isinstance(column, bool):
            return False
        if column < 0 or column >= self.cols:
            return False
        return self.grid[0][column] == EMPTY
    def drop_disc(self, column, symbol):
        """Drop `symbol` into `column`; return the row index where it lands.
        Raises ValueError if the column is out of range or already full.
        """
        if not self.is_valid_column(column):
            raise ValueError("Cannot drop disc into column {}.".format(column))
        for row in range(self.rows - 1, -1, -1):
            if self.grid[row][column] == EMPTY:
                self.grid[row][column] = symbol
                return row
        raise ValueError("Column {} is full.".format(column))
    def is_full(self):
        """Return True when every top cell is occupied, i.e. the grid is full."""
        return all(self.grid[0][col] != EMPTY for col in range(self.cols))
    def check_win(self, row, col, symbol):
        """Return True if the disc at (row, col) completes a line of CONNECT discs.
        Checks horizontal, vertical, and both diagonal directions by counting
        consecutive matching symbols outward from the last placed disc.
        """
        directions = ((0, 1), (1, 0), (1, 1), (1, -1))
        for delta_row, delta_col in directions:
            count = 1
            for step in (1, -1):
                next_row = row + step * delta_row
                next_col = col + step * delta_col
                while (0 <= next_row < self.rows
                       and 0 <= next_col < self.cols
                       and self.grid[next_row][next_col] == symbol):
                    count += 1
                    next_row += step * delta_row
                    next_col += step * delta_col
            if count >= CONNECT:
                return True
        return False
    def display(self):
        """Print the current grid with column numbers aligned over each column."""
        print()
        print(' ' + ' '.join(str(col + 1) for col in range(self.cols)))
        print('+' + '-' * (2 * self.cols - 1) + '+')
        for row in self.grid:
            print('|' + ' '.join(row) + '|')
        print('+' + '-' * (2 * self.cols - 1) + '+')
        print()