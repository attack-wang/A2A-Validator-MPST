'''
board.py
Defines the Board class: stores the Connect Four grid, drops discs,
renders the board, and detects wins and draws.
'''
class Board:
    """A six-row, seven-column Connect Four grid."""
    def __init__(self, rows=6, columns=7):
        """Initialize an empty grid filled with spaces."""
        self.rows = rows
        self.columns = columns
        self.grid = [[" " for _ in range(columns)] for _ in range(rows)]
    def is_valid_column(self, column):
        """Return True if the 0-based column index is in range."""
        return 0 <= column < self.columns
    def has_empty_slot(self, column):
        """Return True if the top cell of the column is still empty."""
        return self.is_valid_column(column) and self.grid[0][column] == " "
    def drop_disc(self, column, disc):
        """Place a disc in the lowest empty row of the column.
        Returns the row index where the disc landed, or None if the
        column is invalid or full.
        """
        if not self.has_empty_slot(column):
            return None
        for row in range(self.rows - 1, -1, -1):
            if self.grid[row][column] == " ":
                self.grid[row][column] = disc
                return row
        return None
    def is_full(self):
        """Return True when every top cell is occupied (draw condition)."""
        return all(self.grid[0][c] != " " for c in range(self.columns))
    def check_win(self, row, col, disc):
        """Return True if the disc at (row, col) completes a line of four.
        Checks horizontal, vertical, and both diagonal directions by
        counting matching discs outward from the last move.
        """
        directions = [(0, 1), (1, 0), (1, 1), (1, -1)]
        for dr, dc in directions:
            count = 1
            for sign in (1, -1):
                r, c = row + sign * dr, col + sign * dc
                while (0 <= r < self.rows and 0 <= c < self.columns
                       and self.grid[r][c] == disc):
                    count += 1
                    r += sign * dr
                    c += sign * dc
            if count >= 4:
                return True
        return False
    def render(self):
        """Print the current grid with column numbers 1-7 underneath."""
        print()
        for row in self.grid:
            print("| " + " | ".join(row) + " |")
        print("|" + "---|" * self.columns)
        print("  " + "   ".join(str(c + 1) for c in range(self.columns)))
        print()