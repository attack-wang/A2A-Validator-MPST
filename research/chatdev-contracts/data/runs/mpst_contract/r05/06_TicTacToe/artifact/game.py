"""Core tic-tac-toe game logic: board state, turns, and win detection."""

WIN_LINES = [
    (0, 1, 2), (3, 4, 5), (6, 7, 8),  # rows
    (0, 3, 6), (1, 4, 7), (2, 5, 8),  # columns
    (0, 4, 8), (2, 4, 6),             # diagonals
]


class TicTacToe:
    """Tracks the 3x3 board, alternating X/O turns, and end conditions."""

    def __init__(self):
        self.reset()

    def reset(self):
        self.board = [" "] * 9
        self.current = "X"
        self.moves = []  # history of (player, position) pairs

    @property
    def current_player(self):
        return self.current

    def available_moves(self):
        return [i for i, cell in enumerate(self.board) if cell == " "]

    def is_valid_move(self, position):
        return position in self.available_moves()

    def make_move(self, position):
        """Place the current player's mark at position (0-8). True on success."""
        if not self.is_valid_move(position):
            return False
        self.board[position] = self.current
        self.moves.append((self.current, position))
        self.current = "O" if self.current == "X" else "X"
        return True

    def check_winner(self):
        """Return 'X'/'O' if won, 'Draw' if board is full, else None."""
        for a, b, c in WIN_LINES:
            if self.board[a] != " " and self.board[a] == self.board[b] == self.board[c]:
                return self.board[a]
        if not self.available_moves():
            return "Draw"
        return None

    def winning_line(self):
        """Return the winning triple of positions, or None."""
        for a, b, c in WIN_LINES:
            if self.board[a] != " " and self.board[a] == self.board[b] == self.board[c]:
                return (a, b, c)
        return None

    def is_full(self):
        return not self.available_moves()