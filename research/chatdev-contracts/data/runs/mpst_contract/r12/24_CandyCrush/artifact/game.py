import random

COLORS = ["#FF4D6D", "#FFD166", "#06D6A0", "#4CC9F0", "#B388EB"]


class Board:
    def __init__(self, size=8, kinds=5):
        self.size = size
        self.kinds = kinds
        self.score = 0
        self.moves = 0
        self.grid = [[None] * size for _ in range(size)]
        self._fill()

    def in_bounds(self, r, c):
        return 0 <= r < self.size and 0 <= c < self.size

    def _fill(self):
        for r in range(self.size):
            for c in range(self.size):
                while True:
                    k = random.randrange(self.kinds)
                    if c >= 2 and self.grid[r][c - 1] == k and self.grid[r][c - 2] == k:
                        continue
                    if r >= 2 and self.grid[r - 1][c] == k and self.grid[r - 2][c] == k:
                        continue
                    self.grid[r][c] = k
                    break

    def find_matches(self, grid=None):
        g = grid if grid is not None else self.grid
        n = self.size
        matches = set()
        for r in range(n):
            run = 1
            for c in range(1, n + 1):
                if c < n and g[r][c] is not None and g[r][c] == g[r][c - 1]:
                    run += 1
                else:
                    if run >= 3:
                        matches.update((r, x) for x in range(c - run, c))
                    run = 1
        for c in range(n):
            run = 1
            for r in range(1, n + 1):
                if r < n and g[r][c] is not None and g[r][c] == g[r - 1][c]:
                    run += 1
                else:
                    if run >= 3:
                        matches.update((x, c) for x in range(r - run, r))
                    run = 1
        return matches

    def try_swap(self, r1, c1, r2, c2):
        if not (self.in_bounds(r1, c1) and self.in_bounds(r2, c2)):
            return False
        if abs(r1 - r2) + abs(c1 - c2) != 1:
            return False
        g = self.grid
        g[r1][c1], g[r2][c2] = g[r2][c2], g[r1][c1]
        if self.find_matches():
            self.moves += 1
            return True
        g[r1][c1], g[r2][c2] = g[r2][c2], g[r1][c1]
        return False

    def resolve(self):
        chain = 0
        events = []
        while True:
            m = self.find_matches()
            if not m:
                break
            chain += 1
            gained = len(m) * 10 * chain
            self.score += gained
            events.append((chain, sorted(m), gained))
            for r, c in m:
                self.grid[r][c] = None
            self._gravity()
        return events

    def _gravity(self):
        n = self.size
        for c in range(n):
            col = [self.grid[r][c] for r in range(n) if self.grid[r][c] is not None]
            col = [random.randrange(self.kinds) for _ in range(n - len(col))] + col
            for r in range(n):
                self.grid[r][c] = col[r]

    def has_moves(self, grid=None):
        g = grid if grid is not None else self.grid
        n = self.size
        for r in range(n):
            for c in range(n):
                for dr, dc in ((0, 1), (1, 0)):
                    r2, c2 = r + dr, c + dc
                    if r2 < n and c2 < n:
                        g[r][c], g[r2][c2] = g[r2][c2], g[r][c]
                        ok = bool(self.find_matches(g))
                        g[r][c], g[r2][c2] = g[r2][c2], g[r][c]
                        if ok:
                            return True
        return False

    def shuffle(self):
        for _ in range(200):
            flat = [k for row in self.grid for k in row]
            random.shuffle(flat)
            g = [flat[i * self.size:(i + 1) * self.size] for i in range(self.size)]
            if not self.find_matches(g) and self.has_moves(g):
                self.grid = g
                return True
        return False