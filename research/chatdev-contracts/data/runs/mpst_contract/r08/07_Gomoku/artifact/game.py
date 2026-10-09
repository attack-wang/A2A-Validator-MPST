"""Gomoku game logic: board state, move validation, and win detection."""

BOARD_SIZE = 15
EMPTY = 0
BLACK = 1
WHITE = 2
WIN_LENGTH = 5

# Directions: horizontal, vertical, diagonal down-right, diagonal down-left
DIRECTIONS = [(0, 1), (1, 0), (1, 1), (1, -1)]

SYMBOLS = {EMPTY: ".", BLACK: "X", WHITE: "O"}


class Board:
    """15x15 Gomoku board with placement and five-in-a-row detection."""

    def __init__(self, size=BOARD_SIZE):
        self.size = size
        self.grid = [[EMPTY] * size for _ in range(size)]
        self.moves_played = 0

    def in_bounds(self, row, col):
        return 0 <= row < self.size and 0 <= col < self.size

    def is_empty(self, row, col):
        return self.grid[row][col] == EMPTY

    def is_full(self):
        return self.moves_played >= self.size * self.size

    def place(self, row, col, player):
        """Place a stone if the cell is valid and empty. Return True on success."""
        if not self.in_bounds(row, col) or not self.is_empty(row, col):
            return False
        self.grid[row][col] = player
        self.moves_played += 1
        return True

    def check_win(self, row, col):
        """Return the player who has five in a row through (row, col), else EMPTY."""
        player = self.grid[row][col]
        if player == EMPTY:
            return EMPTY
        for dr, dc in DIRECTIONS:
            count = 1
            for sign in (1, -1):
                r, c = row + sign * dr, col + sign * dc
                while self.in_bounds(r, c) and self.grid[r][c] == player:
                    count += 1
                    r += sign * dr
                    c += sign * dc
            if count >= WIN_LENGTH:
                return player
        return EMPTY

    def render(self):
        """Return a string representation of the board with indices."""
        header = "   " + " ".join(str(c % 10) for c in range(self.size))
        lines = [header]
        for r in range(self.size):
            lines.append(f"{r:2d} " + " ".join(SYMBOLS[v] for v in self.grid[r]))
        return "\n".join(lines)