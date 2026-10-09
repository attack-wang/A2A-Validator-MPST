"""Gomoku game logic: board state, move validation, and win detection."""

BOARD_SIZE = 15
EMPTY = "."
BLACK = "X"
WHITE = "O"
DIRECTIONS = ((0, 1), (1, 0), (1, 1), (1, -1))


class Board:
    """15x15 Gomoku board with stone placement and five-in-a-row detection."""

    def __init__(self, size=BOARD_SIZE):
        self.size = size
        self.grid = [[EMPTY] * size for _ in range(size)]
        self.moves_played = 0

    def in_bounds(self, row, col):
        return 0 <= row < self.size and 0 <= col < self.size

    def is_empty(self, row, col):
        return self.grid[row][col] == EMPTY

    def place(self, row, col, stone):
        """Place a stone; returns True on success, False on an invalid move."""
        if not self.in_bounds(row, col) or not self.is_empty(row, col):
            return False
        self.grid[row][col] = stone
        self.moves_played += 1
        return True

    def is_full(self):
        return self.moves_played >= self.size * self.size

    def winning_line(self, row, col):
        """Return the 5-cell winning line through (row, col), or None."""
        stone = self.grid[row][col]
        if stone == EMPTY:
            return None
        for dr, dc in DIRECTIONS:
            cells = [(row, col)]
            for sign in (1, -1):
                r, c = row + sign * dr, col + sign * dc
                while self.in_bounds(r, c) and self.grid[r][c] == stone:
                    cells.append((r, c))
                    r += sign * dr
                    c += sign * dc
            if len(cells) >= 5:
                cells.sort()
                return cells[:5]
        return None

    def render(self, highlight=None):
        """Return the board as a string; highlighted cells are shown in brackets."""
        highlight = highlight or set()
        lines = ["   " + " ".join(chr(ord("A") + c) for c in range(self.size))]
        for r in range(self.size):
            cells = []
            for c in range(self.size):
                ch = self.grid[r][c]
                cells.append("[" + ch + "]" if (r, c) in highlight else ch)
            lines.append(f"{r + 1:2d} " + " ".join(cells))
        return "\n".join(lines)