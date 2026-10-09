"""Connect Four game logic: board, moves, and win detection."""

ROWS = 6
COLS = 7
EMPTY = "."
PLAYERS = ("X", "O")


class ConnectFour:
    """Seven-column, six-row grid where discs fall to the lowest empty cell."""

    def __init__(self):
        self.board = [[EMPTY] * COLS for _ in range(ROWS)]
        self.current = 0  # index into PLAYERS

    def display(self):
        """Print the board with column numbers."""
        header = " ".join(str(c + 1) for c in range(COLS))
        print("\n" + header)
        for row in self.board:
            print(" ".join(row))
        print(header)

    def is_valid_column(self, col):
        """A column is valid if it is in range and not full."""
        return 0 <= col < COLS and self.board[0][col] == EMPTY

    def drop_disc(self, col):
        """Place the current player's disc in col; return the landing row."""
        for r in range(ROWS - 1, -1, -1):
            if self.board[r][col] == EMPTY:
                self.board[r][col] = PLAYERS[self.current]
                return r
        return -1

    def check_win(self, row, col):
        """True if the disc at (row, col) completes a line of four."""
        player = self.board[row][col]
        directions = ((0, 1), (1, 0), (1, 1), (1, -1))
        for dr, dc in directions:
            count = 1
            for sign in (1, -1):
                r, c = row + dr * sign, col + dc * sign
                while (
                    0 <= r < ROWS
                    and 0 <= c < COLS
                    and self.board[r][c] == player
                ):
                    count += 1
                    r += dr * sign
                    c += dc * sign
            if count >= 4:
                return True
        return False

    def is_full(self):
        """The grid is full when the top row has no empty cells."""
        return all(self.board[0][c] != EMPTY for c in range(COLS))

    def switch_player(self):
        self.current = 1 - self.current