"""Connect Four game logic: board state, move validation, and win detection."""

ROWS = 6
COLS = 7
EMPTY = "."


class Board:
    """Seven-column, six-row grid where discs fall to the lowest empty cell."""

    def __init__(self):
        self.grid = [[EMPTY for _ in range(COLS)] for _ in range(ROWS)]

    def display(self):
        header = " ".join(str(c + 1) for c in range(COLS))
        print("\n" + header)
        for row in self.grid:
            print(" ".join(row))
        print(header)

    def is_valid_column(self, col):
        """A column is playable if it is in range and its top cell is empty."""
        return 0 <= col < COLS and self.grid[0][col] == EMPTY

    def drop_disc(self, col, disc):
        """Place a disc in the lowest empty row of the column; return its row."""
        for r in range(ROWS - 1, -1, -1):
            if self.grid[r][col] == EMPTY:
                self.grid[r][col] = disc
                return r
        return -1

    def is_full(self):
        return all(self.grid[0][c] != EMPTY for c in range(COLS))

    def check_win(self, disc):
        """True if the disc forms a horizontal, vertical, or diagonal four."""
        # Horizontal
        for r in range(ROWS):
            for c in range(COLS - 3):
                if all(self.grid[r][c + i] == disc for i in range(4)):
                    return True
        # Vertical
        for c in range(COLS):
            for r in range(ROWS - 3):
                if all(self.grid[r + i][c] == disc for i in range(4)):
                    return True
        # Diagonal down-right
        for r in range(ROWS - 3):
            for c in range(COLS - 3):
                if all(self.grid[r + i][c + i] == disc for i in range(4)):
                    return True
        # Diagonal up-right
        for r in range(3, ROWS):
            for c in range(COLS - 3):
                if all(self.grid[r - i][c + i] == disc for i in range(4)):
                    return True
        return False