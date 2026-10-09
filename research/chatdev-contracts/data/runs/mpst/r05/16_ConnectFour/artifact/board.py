'''
board.py
Defines the Board class for the Connect Four game.
The Board stores a 6-row by 7-column grid, drops discs with gravity,
validates column choices, renders the grid to the console and detects
winning lines (horizontal, vertical or diagonal) as well as draws.
'''
class Board:
    """Connect Four grid with disc dropping, rendering and win detection."""
    EMPTY = "."
    def __init__(self, rows=6, cols=7):
        """Create an empty rows x cols grid (row 0 is the top row)."""
        self.rows = rows
        self.cols = cols
        self.grid = [[self.EMPTY for _ in range(cols)] for _ in range(rows)]
    def is_valid_column(self, col):
        """Return True if col is inside the grid and not already full."""
        return 0 <= col < self.cols and self.grid[0][col] == self.EMPTY
    def drop_disc(self, col, disc):
        """
        Drop a disc into column col (0-based).
        The disc falls to the lowest empty row. Returns the (row, col)
        position where it landed, or None if the column is invalid or full.
        """
        if not self.is_valid_column(col):
            return None
        for row in range(self.rows - 1, -1, -1):
            if self.grid[row][col] == self.EMPTY:
                self.grid[row][col] = disc
                return row, col
        return None
    def is_full(self):
        """Return True when every cell is occupied (draw condition)."""
        return all(self.grid[0][col] != self.EMPTY for col in range(self.cols))
    def check_win(self, row, col, disc):
        """
        Return True if the disc just placed at (row, col) completes a
        line of four or more identical discs horizontally, vertically
        or diagonally.
        """
        directions = ((0, 1), (1, 0), (1, 1), (1, -1))
        for d_row, d_col in directions:
            count = 1
            r, c = row + d_row, col + d_col
            while 0 <= r < self.rows and 0 <= c < self.cols and self.grid[r][c] == disc:
                count += 1
                r += d_row
                c += d_col
            r, c = row - d_row, col - d_col
            while 0 <= r < self.rows and 0 <= c < self.cols and self.grid[r][c] == disc:
                count += 1
                r -= d_row
                c -= d_col
            if count >= 4:
                return True
        return False
    def render(self):
        """Print the current grid with column numbers 1..cols above it."""
        header = " ".join(str(number) for number in range(1, self.cols + 1))
        print("  " + header)
        for row in self.grid:
            print("| " + " ".join(row) + " |")
        print("+" + "-" * (2 * self.cols + 1) + "+")