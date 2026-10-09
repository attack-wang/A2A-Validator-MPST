'''
board.py
Defines the Board class for the Connect Four game. It manages the
six-row by seven-column grid, validates column choices, drops discs
into the lowest available cell, and detects winning lines
(horizontal, vertical, and both diagonals) as well as draw conditions.
'''
class Board:
    """Represents the Connect Four grid and implements its core rules."""
    EMPTY = ' '
    ROWS = 6
    COLS = 7
    WIN_LENGTH = 4
    def __init__(self, rows=ROWS, cols=COLS):
        """Create an empty grid with the given dimensions."""
        self.rows = rows
        self.cols = cols
        self.grid = [[Board.EMPTY for _ in range(cols)] for _ in range(rows)]
    def is_valid_column(self, col):
        """Return True if col is inside the grid and not already full."""
        return 0 <= col < self.cols and self.grid[0][col] == Board.EMPTY
    def drop_disc(self, col, disc):
        """Place a disc in the lowest empty cell of the given column.
        Returns the row index where the disc landed, or None if the
        column is out of range or full.
        """
        if not self.is_valid_column(col):
            return None
        for row in range(self.rows - 1, -1, -1):
            if self.grid[row][col] == Board.EMPTY:
                self.grid[row][col] = disc
                return row
        return None
    def is_full(self):
        """Return True when every column is full (draw condition)."""
        return all(self.grid[0][col] != Board.EMPTY for col in range(self.cols))
    def get_valid_columns(self):
        """Return a list of column indices that can still accept a disc."""
        return [col for col in range(self.cols) if self.is_valid_column(col)]
    def check_win(self, row, col, disc):
        """Return True if the disc at (row, col) completes a line of four.
        Checks horizontal, vertical, and both diagonal directions
        radiating out from the last placed disc.
        """
        directions = ((0, 1), (1, 0), (1, 1), (1, -1))
        for dr, dc in directions:
            count = 1
            for sign in (1, -1):
                r, c = row + sign * dr, col + sign * dc
                while (0 <= r < self.rows and 0 <= c < self.cols
                       and self.grid[r][c] == disc):
                    count += 1
                    r += sign * dr
                    c += sign * dc
            if count >= Board.WIN_LENGTH:
                return True
        return False
    def display(self):
        """Print the current state of the board to the console."""
        print(' ' + ' '.join(str(col + 1) for col in range(self.cols)))
        for row_cells in self.grid:
            print('|' + '|'.join(row_cells) + '|')
        print('+' + '-' * (2 * self.cols - 1) + '+')