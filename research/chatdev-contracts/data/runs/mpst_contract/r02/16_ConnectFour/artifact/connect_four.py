"""Connect Four game logic: board state, move handling, and win detection."""

ROWS = 6
COLS = 7
EMPTY = "."
DISCS = ("X", "O")


class ConnectFour:
    """Seven-column, six-row Connect Four board for two players."""

    def __init__(self):
        self.board = [[EMPTY for _ in range(COLS)] for _ in range(ROWS)]
        self.current = 0  # index into DISCS

    @property
    def disc(self):
        """Disc symbol of the player whose turn it is."""
        return DISCS[self.current]

    def display(self):
        """Print the board with column numbers above and below."""
        header = " ".join(str(c + 1) for c in range(COLS))
        print(header)
        for row in self.board:
            print(" ".join(row))
        print(header)

    def is_valid_column(self, col):
        """A column is playable if it is in range and not full."""
        return 0 <= col < COLS and self.board[0][col] == EMPTY

    def drop_disc(self, col):
        """Drop the current player's disc into col; return the landing row."""
        for r in range(ROWS - 1, -1, -1):
            if self.board[r][col] == EMPTY:
                self.board[r][col] = self.disc
                return r
        raise ValueError("Column is full.")

    def check_win(self, row, col):
        """True if the disc at (row, col) completes a line of four."""
        player = self.board[row][col]
        for dr, dc in ((0, 1), (1, 0), (1, 1), (1, -1)):
            count = 1
            for sign in (1, -1):
                r, c = row + sign * dr, col + sign * dc
                while 0 <= r < ROWS and 0 <= c < COLS and self.board[r][c] == player:
                    count += 1
                    r += sign * dr
                    c += sign * dc
            if count >= 4:
                return True
        return False

    def is_full(self):
        """The grid is full when every top cell is occupied."""
        return all(self.board[0][c] != EMPTY for c in range(COLS))

    def switch_player(self):
        self.current = 1 - self.current