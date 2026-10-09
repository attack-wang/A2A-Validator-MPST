"""Core tic-tac-toe game logic: board, turns, and win/draw detection."""

WIN_LINES = [
    (0, 1, 2), (3, 4, 5), (6, 7, 8),  # rows
    (0, 3, 6), (1, 4, 7), (2, 5, 8),  # columns
    (0, 4, 8), (2, 4, 6),             # diagonals
]


class TicTacToe:
    """Tracks a 3x3 board, the current player, and game-over conditions."""

    def __init__(self):
        self.board = [" "] * 9
        self.current_player = "X"
        self.moves_made = 0

    def make_move(self, position):
        """Place the current player's mark at position (1-9). Return True on success."""
        if not self.is_valid_move(position):
            return False
        self.board[position - 1] = self.current_player
        self.moves_made += 1
        return True

    def is_valid_move(self, position):
        return isinstance(position, int) and 1 <= position <= 9 and self.board[position - 1] == " "

    def switch_player(self):
        self.current_player = "O" if self.current_player == "X" else "X"

    def check_winner(self):
        """Return the winning mark ('X' or 'O'), or None if there is no winner yet."""
        for a, b, c in WIN_LINES:
            if self.board[a] != " " and self.board[a] == self.board[b] == self.board[c]:
                return self.board[a]
        return None

    def winning_line(self):
        """Return the winning triple of 1-based positions, or None."""
        for a, b, c in WIN_LINES:
            if self.board[a] != " " and self.board[a] == self.board[b] == self.board[c]:
                return (a + 1, b + 1, c + 1)
        return None

    def is_full(self):
        return self.moves_made == 9

    def is_over(self):
        return self.check_winner() is not None or self.is_full()