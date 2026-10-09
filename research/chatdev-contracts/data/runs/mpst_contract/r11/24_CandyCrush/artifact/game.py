import random

COLORS = "ROYGBP"


class Board:
    def __init__(self, rows=8, cols=8, seed=None):
        self.rows, self.cols = rows, cols
        self.rng = random.Random(seed)
        self.grid = [[self.rng.choice(COLORS) for _ in range(cols)] for _ in range(rows)]
        self.score = 0
        self.moves = 0
        while self.find_matches():
            self.resolve()
        while not self.has_valid_move():
            self.shuffle()

    def in_bounds(self, r, c):
        return 0 <= r < self.rows and 0 <= c < self.cols

    def find_matches(self):
        matches = set()
        for r in range(self.rows):
            c = 0
            while c < self.cols - 2:
                v = self.grid[r][c]
                if v and v == self.grid[r][c + 1] == self.grid[r][c + 2]:
                    k = c
                    while k < self.cols and self.grid[r][k] == v:
                        matches.add((r, k))
                        k += 1
                    c = k
                else:
                    c += 1
        for c in range(self.cols):
            r = 0
            while r < self.rows - 2:
                v = self.grid[r][c]
                if v and v == self.grid[r + 1][c] == self.grid[r + 2][c]:
                    k = r
                    while k < self.rows and self.grid[k][c] == v:
                        matches.add((k, c))
                        k += 1
                    r = k
                else:
                    r += 1
        return matches

    def swap(self, r1, c1, r2, c2):
        if not (self.in_bounds(r1, c1) and self.in_bounds(r2, c2)):
            return False
        if abs(r1 - r2) + abs(c1 - c2) != 1:
            return False
        self.grid[r1][c1], self.grid[r2][c2] = self.grid[r2][c2], self.grid[r1][c1]
        if self.find_matches():
            return True
        self.grid[r1][c1], self.grid[r2][c2] = self.grid[r2][c2], self.grid[r1][c1]
        return False

    def apply_gravity(self):
        for c in range(self.cols):
            write = self.rows - 1
            for r in range(self.rows - 1, -1, -1):
                if self.grid[r][c] is not None:
                    self.grid[r][c], self.grid[write][c] = self.grid[write][c], self.grid[r][c]
                    write -= 1
            for r in range(write, -1, -1):
                self.grid[r][c] = self.rng.choice(COLORS)

    def resolve(self):
        total, chain = 0, 0
        while True:
            matches = self.find_matches()
            if not matches:
                break
            chain += 1
            total += len(matches) * 10 * chain
            for r, c in matches:
                self.grid[r][c] = None
            self.apply_gravity()
        return total, chain

    def has_valid_move(self):
        for r in range(self.rows):
            for c in range(self.cols):
                for dr, dc in ((0, 1), (1, 0)):
                    r2, c2 = r + dr, c + dc
                    if self.in_bounds(r2, c2):
                        self.grid[r][c], self.grid[r2][c2] = self.grid[r2][c2], self.grid[r][c]
                        ok = bool(self.find_matches())
                        self.grid[r][c], self.grid[r2][c2] = self.grid[r2][c2], self.grid[r][c]
                        if ok:
                            return True
        return False

    def shuffle(self):
        cells = [self.grid[r][c] for r in range(self.rows) for c in range(self.cols)]
        while True:
            for _ in range(200):
                self.rng.shuffle(cells)
                it = iter(cells)
                self.grid = [[next(it) for _ in range(self.cols)] for _ in range(self.rows)]
                if not self.find_matches() and self.has_valid_move():
                    return
            while self.find_matches():
                self.resolve()

    def move(self, r1, c1, r2, c2):
        if not self.swap(r1, c1, r2, c2):
            return None
        gained, chain = self.resolve()
        self.score += gained
        self.moves += 1
        while not self.has_valid_move():
            self.shuffle()
        return gained, chain