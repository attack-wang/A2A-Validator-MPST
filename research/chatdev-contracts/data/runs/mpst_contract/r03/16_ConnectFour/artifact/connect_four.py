"""Core Connect Four game logic: board state, moves, and win detection."""

ROWS = 6
COLS = 7
EMPTY = "."


class ConnectFour:
    """Standard Connect Four board: 6 rows x 7 columns, two players."""

    def __init__(self):
        self.board = [[EMPTY for _ in range(COLS)] for _ in range(ROWS)]
        self.current_player = 1

    @staticmethod
    def disc(player):
        """Return the disc symbol for a player number."""
        return "X" if player == 1 else "O"

    def display(self):
        """Return the board as a string with a column-number header."""
        header = " ".join(str(c + 1) for c in range(COLS))
        rows = [" ".join(row) for row in self.board]
        return "\n".join([header] + rows)

    def is_valid_column(self, col):
        """True if col (0-based) is in range and not already full."""
        return 0 <= col < COLS and self.board[0][col] == EMPTY

    def drop_disc(self, col):
        """Drop the current player's disc into col (0-based). Returns True on success."""
        if not self.is_valid_column(col):
            return False
        for r in range(ROWS - 1, -1, -1):
            if self.board[r][col] == EMPTY:
                self.board[r][col] = self.disc(self.current_player)
                return True
        return False

    def switch_player(self):
        """Alternate turns between player 1 and player 2."""
        self.current_player = 3 - self.current_player

    def check_win(self):
        """Return the winning disc symbol if four-in-a-row exists, else None."""
        for r in range(ROWS):
            for c in range(COLS):
                disc = self.board[r][c]
                if disc == EMPTY:
                    continue
                for dr, dc in ((0, 1), (1, 0), (1, 1), (1, -1)):
                    if self._line_from(r, c, dr, dc, disc):
                        return disc
        return None

    def _line_from(self, r, c, dr, dc, disc):
        """True if four identical discs start at (r, c) along direction (dr, dc)."""
        for i in range(4):
            rr, cc = r + dr * i, c + dc * i
            if not (0 <= rr < ROWS and 0 <= cc < COLS) or self.board[rr][cc] != disc:
                return False
        return True

    def is_full(self):
        """True when every column is filled (draw condition)."""
        return all(self.board[0][c] != EMPTY for c in range(COLS))