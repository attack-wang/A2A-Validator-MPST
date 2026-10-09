"""Connect Four game logic: 6-row, 7-column grid, four-in-a-line wins."""

ROWS = 6
COLS = 7


class ConnectFour:
    """Grid state, disc dropping, and win/draw detection for Connect Four."""

    def __init__(self):
        self.grid = [[0] * COLS for _ in range(ROWS)]  # 0 empty, 1/2 players
        self.current = 1

    def drop(self, col):
        """Place current player's disc in 0-based column; return row or None if full."""
        for row in range(ROWS - 1, -1, -1):
            if self.grid[row][col] == 0:
                self.grid[row][col] = self.current
                return row
        return None

    def is_full(self, col):
        return self.grid[0][col] != 0

    def full(self):
        return all(self.grid[0][c] != 0 for c in range(COLS))

    def check_win(self, row, col):
        """True if the disc at (row, col) completes a line of four or more."""
        player = self.grid[row][col]
        for dr, dc in ((0, 1), (1, 0), (1, 1), (1, -1)):
            count = 1
            for sign in (1, -1):
                r, c = row + dr * sign, col + dc * sign
                while 0 <= r < ROWS and 0 <= c < COLS and self.grid[r][c] == player:
                    count += 1
                    r += dr * sign
                    c += dc * sign
            if count >= 4:
                return True
        return False

    def switch(self):
        self.current = 3 - self.current