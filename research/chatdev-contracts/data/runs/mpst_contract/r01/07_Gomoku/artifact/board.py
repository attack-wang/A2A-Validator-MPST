SIZE = 15
EMPTY, BLACK, WHITE = 0, 1, 2
SYMBOLS = {EMPTY: ".", BLACK: "X", WHITE: "O"}
DIRECTIONS = ((0, 1), (1, 0), (1, 1), (1, -1))


class Board:
    def __init__(self):
        self.grid = [[EMPTY] * SIZE for _ in range(SIZE)]

    def in_bounds(self, r, c):
        return 0 <= r < SIZE and 0 <= c < SIZE

    def is_empty(self, r, c):
        return self.in_bounds(r, c) and self.grid[r][c] == EMPTY

    def place(self, r, c, player):
        self.grid[r][c] = player

    def check_win(self, r, c):
        player = self.grid[r][c]
        if player == EMPTY:
            return False
        for dr, dc in DIRECTIONS:
            count = 1
            for sign in (1, -1):
                nr, nc = r + sign * dr, c + sign * dc
                while self.in_bounds(nr, nc) and self.grid[nr][nc] == player:
                    count += 1
                    nr += sign * dr
                    nc += sign * dc
            if count >= 5:
                return True
        return False

    def is_full(self):
        return all(self.grid[r][c] != EMPTY for r in range(SIZE) for c in range(SIZE))

    def display(self):
        print("   " + " ".join(f"{c + 1:2d}" for c in range(SIZE)))
        for r in range(SIZE):
            row = " ".join(f"{SYMBOLS[self.grid[r][c]]:2s}" for c in range(SIZE))
            print(f"{r + 1:2d} {row}")