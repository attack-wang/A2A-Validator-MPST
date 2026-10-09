"""Gomoku board: state, placement, win detection, rendering."""

SIZE = 15
EMPTY, BLACK, WHITE = 0, 1, 2
SYMBOLS = {EMPTY: ".", BLACK: "X", WHITE: "O"}
DIRECTIONS = ((0, 1), (1, 0), (1, 1), (1, -1))  # H, V, diag \, diag /


class Board:
    def __init__(self, size=SIZE):
        self.size = size
        self.grid = [[EMPTY] * size for _ in range(size)]

    def in_bounds(self, r, c):
        return 0 <= r < self.size and 0 <= c < self.size

    def is_empty(self, r, c):
        return self.grid[r][c] == EMPTY

    def place(self, r, c, player):
        self.grid[r][c] = player

    def is_full(self):
        return all(cell != EMPTY for row in self.grid for cell in row)

    def check_win(self, r, c, player):
        """True if the stone at (r, c) completes a line of 5+ for player."""
        for dr, dc in DIRECTIONS:
            count = 1
            for sign in (1, -1):
                nr, nc = r + dr * sign, c + dc * sign
                while self.in_bounds(nr, nc) and self.grid[nr][nc] == player:
                    count += 1
                    nr += dr * sign
                    nc += dc * sign
            if count >= 5:
                return True
        return False

    def render(self):
        header = "   " + " ".join(f"{c:2d}" for c in range(self.size))
        lines = [header]
        for r in range(self.size):
            row = " ".join(f"{SYMBOLS[v]:>2}" for v in self.grid[r])
            lines.append(f"{r:2d} {row}")
        return "\n".join(lines)