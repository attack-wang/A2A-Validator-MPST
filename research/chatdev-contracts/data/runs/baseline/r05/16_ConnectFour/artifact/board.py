'''
board.py
Defines the Board class that manages the 6x7 Connect Four grid,
disc placement, win detection, and draw detection.
'''
class Board:
    """Represents the Connect Four grid and the rules for placing discs."""
    def __init__(self, rows=6, cols=7):
        """Create an empty grid with the given number of rows and columns."""
        self.rows = rows
        self.cols = cols
        # grid[row][col]; None means empty, otherwise holds the disc symbol
        self.grid = [[None for _ in range(cols)] for _ in range(rows)]
    def is_valid_column(self, col):
        """Return True if col is inside the grid and the column is not full."""
        return 0 <= col < self.cols and self.grid[0][col] is None
    def drop_disc(self, col, disc):
        """Place a disc into the lowest empty cell of the given column.
        Returns the row index where the disc landed, or None if the
        column is out of range or already full.
        """
        if not self.is_valid_column(col):
            return None
        for row in range(self.rows - 1, -1, -1):
            if self.grid[row][col] is None:
                self.grid[row][col] = disc
                return row
        return None
    def check_win(self, row, col, disc):
        """Return True if the disc placed at (row, col) completes a
        horizontal, vertical, or diagonal line of four identical discs."""
        directions = [(0, 1), (1, 0), (1, 1), (1, -1)]
        for dr, dc in directions:
            count = 1  # the disc just placed
            # Extend in the positive direction along this axis
            r, c = row + dr, col + dc
            while 0 <= r < self.rows and 0 <= c < self.cols and self.grid[r][c] == disc:
                count += 1
                r += dr
                c += dc
            # Extend in the negative direction along this axis
            r, c = row - dr, col - dc
            while 0 <= r < self.rows and 0 <= c < self.cols and self.grid[r][c] == disc:
                count += 1
                r -= dr
                c -= dc
            if count >= 4:
                return True
        return False
    def is_full(self):
        """Return True when the top row is fully occupied (grid is full)."""
        return all(cell is not None for cell in self.grid[0])