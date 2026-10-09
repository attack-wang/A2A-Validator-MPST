"""Core tic-tac-toe game logic: board state, turns, and win detection."""

WIN_LINES = [
    (0, 1, 2), (3, 4, 5), (6, 7, 8),  # rows
    (0, 3, 6), (1, 4, 7), (2, 5, 8),  # columns
    (0, 4, 8), (2, 4, 6),             # diagonals
]


class TicTacToe:
    """Tracks the 3x3 board, the current player, and end-of-game conditions."""

    def __init__(self):
        self.board = [" "] * 9
        self.current = "X"

    def make_move(self, position):
        """Place the current player's mark at position (1-9). Returns True on success."""
        if not (1 <= position <= 9) or self.board[position - 1] != " ":
            return False
        self.board[position - 1] = self.current
        return True

    def switch_player(self):
        """Alternate turns between X and O."""
        self.current = "O" if self.current == "X" else "X"

    def check_winner(self):
        """Return the winning mark, 'Draw' if the board is full, or None to continue."""
        for a, b, c in WIN_LINES:
            if self.board[a] != " " and self.board[a] == self.board[b] == self.board[c]:
                return self.board[a]
        if " " not in self.board:
            return "Draw"
        return None

    def available_moves(self):
        """Return the list of empty cell positions (1-9)."""
        return [i + 1 for i, cell in enumerate(self.board) if cell == " "]