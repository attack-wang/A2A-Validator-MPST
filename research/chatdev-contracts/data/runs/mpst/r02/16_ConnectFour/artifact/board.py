'''
board.py
Defines the Board class for the Connect Four game.
The Board is responsible for:
  * Storing the 6-row x 7-column grid of discs.
  * Validating column choices (in range and not full).
  * Dropping a disc into a column with gravity (lowest empty cell).
  * Detecting winning lines (horizontal, vertical, both diagonals).
  * Detecting a full grid (draw condition).
  * Rendering the board as text for the console.
'''
class Board:
    """Represents the Connect Four grid and all board-related logic."""
    EMPTY = "."  # Symbol used for empty cells
    # All (row delta, col delta) directions needed to detect a 4-in-a-row:
    # horizontal, vertical, diagonal down-right, diagonal down-left.
    DIRECTIONS = ((0, 1), (1, 0), (1, 1), (1, -1))
    def __init__(self, rows=6, cols=7):
        """Create an empty rows x cols grid filled with EMPTY cells."""
        self.rows = rows
        self.cols = cols
        self.grid = [[Board.EMPTY for _ in range(cols)] for _ in range(rows)]
    def is_valid_column(self, col):
        """Return True if col is inside the grid and not already full."""
        return 0 <= col < self.cols and self.grid[0][col] == Board.EMPTY
    def drop_disc(self, col, disc):
        """
        Drop a disc into the given column.
        The disc falls to the lowest empty row (gravity). Returns the row
        index where the disc landed, or None if the move is invalid.
        """
        if not self.is_valid_column(col):
            return None
        for row in range(self.rows - 1, -1, -1):
            if self.grid[row][col] == Board.EMPTY:
                self.grid[row][col] = disc
                return row
        return None
    def check_win(self, disc):
        """Return True if the given disc has four in a row anywhere."""
        for row in range(self.rows):
            for col in range(self.cols):
                if self.grid[row][col] == disc:
                    for dr, dc in Board.DIRECTIONS:
                        if self._line_from(row, col, dr, dc, disc):
                            return True
        return False
    def _line_from(self, row, col, dr, dc, disc):
        """
        Return True if four identical discs start at (row, col) and
        continue in direction (dr, dc).
        """
        for i in range(4):
            r = row + dr * i
            c = col + dc * i
            if r < 0 or r >= self.rows or c < 0 or c >= self.cols:
                return False
            if self.grid[r][c] != disc:
                return False
        return True
    def is_full(self):
        """Return True when every column is full (draw condition)."""
        return all(self.grid[0][col] != Board.EMPTY for col in range(self.cols))
    def render(self):
        """Print the current grid with column numbers 1..cols."""
        header = " ".join(str(col + 1) for col in range(self.cols))
        border = "+" + "-" * (self.cols * 2 - 1) + "+"
        print()
        print(" " + header)
        print(border)
        for row in self.grid:
            print("|" + " ".join(row) + "|")
        print(border)
        print()