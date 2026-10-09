"""Connect Four game logic: board state, move handling, and win detection."""

ROWS, COLS = 6, 7
EMPTY = "."


class ConnectFour:
    """Seven-column, six-row grid where two players drop alternating discs."""

    def __init__(self):
        self.board = [[EMPTY] * COLS for _ in range(ROWS)]
        self.current = "X"

    def display(self):
        """Print the board with column numbers beneath it."""
        print()
        for row in self.board:
            print(" ".join(row))
        print(" ".join(str(c) for c in range(1, COLS + 1)))
        print()

    def is_valid_column(self, col):
        """A column is valid if it is in range and its top cell is empty."""
        return 0 <= col < COLS and self.board[0][col] == EMPTY

    def drop_disc(self, col):
        """Place the current player's disc in the lowest empty row of col."""
        for r in range(ROWS - 1, -1, -1):
            if self.board[r][col] == EMPTY:
                self.board[r][col] = self.current
                return r
        return -1

    def check_win(self, row, col):
        """True if the disc at (row, col) completes a line of four or more."""
        player = self.board[row][col]
        for dr, dc in ((0, 1), (1, 0), (1, 1), (1, -1)):
            count = 1
            for sign in (1, -1):
                r, c = row + dr * sign, col + dc * sign
                while 0 <= r < ROWS and 0 <= c < COLS and self.board[r][c] == player:
                    count += 1
                    r += dr * sign
                    c += dc * sign
            if count >= 4:
                return True
        return False

    def is_full(self):
        """The grid is full when every top-row cell is occupied."""
        return all(self.board[0][c] != EMPTY for c in range(COLS))

    def switch_player(self):
        """Hand the turn to the other player."""
        self.current = "O" if self.current == "X" else "X"