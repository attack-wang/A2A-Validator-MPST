"""Board logic for Gomoku."""
SIZE = 15
EMPTY, BLACK, WHITE = 0, 1, 2
SYMBOLS = {EMPTY: ".", BLACK: "X", WHITE: "O"}


class Board:
    def __init__(self, size=SIZE):
        self.size = size
        self.grid = [[EMPTY] * size for _ in range(size)]

    def in_bounds(self, r, c):
        return 0 <= r < self.size and 0 <= c < self.size

    def is_empty(self, r, c):
        return self.in_bounds(r, c) and self.grid[r][c] == EMPTY

    def place(self, r, c, stone):
        if not self.is_empty(r, c):
            return False
        self.grid[r][c] = stone
        return True

    def check_win(self, r, c):
        stone = self.grid[r][c]
        if stone == EMPTY:
            return False
        for dr, dc in ((0, 1), (1, 0), (1, 1), (1, -1)):
            count = 1
            for sign in (1, -1):
                nr, nc = r + dr * sign, c + dc * sign
                while self.in_bounds(nr, nc) and self.grid[nr][nc] == stone:
                    count += 1
                    nr += dr * sign
                    nc += dc * sign
            if count >= 5:
                return True
        return False

    def full(self):
        return all(cell != EMPTY for row in self.grid for cell in row)

    def display(self):
        header = "   " + " ".join(f"{c + 1:2d}" for c in range(self.size))
        print(header)
        for r, row in enumerate(self.grid):
            cells = "  ".join(SYMBOLS[cell] for cell in row)
            print(f"{r + 1:2d} {cells}")
        print()