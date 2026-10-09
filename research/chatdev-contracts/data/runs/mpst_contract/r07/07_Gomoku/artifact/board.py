"""Board state and win detection for Gomoku."""

SIZE = 15
EMPTY, BLACK, WHITE = 0, 1, 2


class Board:
    def __init__(self, size=SIZE):
        self.size = size
        self.grid = [[EMPTY] * size for _ in range(size)]

    def in_bounds(self, r, c):
        return 0 <= r < self.size and 0 <= c < self.size

    def is_empty(self, r, c):
        return self.in_bounds(r, c) and self.grid[r][c] == EMPTY

    def place(self, r, c, stone):
        self.grid[r][c] = stone

    def is_full(self):
        return all(v != EMPTY for row in self.grid for v in row)

    def check_win(self, r, c):
        """True if the stone just placed at (r, c) completes five in a row."""
        stone = self.grid[r][c]
        if stone == EMPTY:
            return False
        for dr, dc in ((0, 1), (1, 0), (1, 1), (1, -1)):
            count = 1
            for step in (1, -1):
                nr, nc = r + dr * step, c + dc * step
                while self.in_bounds(nr, nc) and self.grid[nr][nc] == stone:
                    count += 1
                    nr += dr * step
                    nc += dc * step
            if count >= 5:
                return True
        return False