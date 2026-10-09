import random

COLORS = "ROYGBP"
EMPTY = "."


class Board:
    def __init__(self, size=8, types=6, seed=None):
        self.size = size
        self.types = types
        self.rng = random.Random(seed)
        self.reset()

    def reset(self):
        while True:
            self.grid = [[None] * self.size for _ in range(self.size)]
            for r in range(self.size):
                for c in range(self.size):
                    self.grid[r][c] = self._pick(r, c)
            if self.find_move():
                return

    def _pick(self, r, c):
        while True:
            t = self.rng.randrange(self.types)
            if c >= 2 and self.grid[r][c - 1] == t and self.grid[r][c - 2] == t:
                continue
            if r >= 2 and self.grid[r - 1][c] == t and self.grid[r - 2][c] == t:
                continue
            return t

    def cell(self, t):
        return EMPTY if t is None else COLORS[t]

    def swap(self, a, b):
        (r1, c1), (r2, c2) = a, b
        self.grid[r1][c1], self.grid[r2][c2] = self.grid[r2][c2], self.grid[r1][c1]

    def find_matches(self):
        n, matches = self.size, set()
        for r in range(n):
            c = 0
            while c < n:
                t = self.grid[r][c]
                e = c + 1
                if t is not None:
                    while e < n and self.grid[r][e] == t:
                        e += 1
                    if e - c >= 3:
                        matches.update((r, x) for x in range(c, e))
                c = e
        for c in range(n):
            r = 0
            while r < n:
                t = self.grid[r][c]
                e = r + 1
                if t is not None:
                    while e < n and self.grid[e][c] == t:
                        e += 1
                    if e - r >= 3:
                        matches.update((x, c) for x in range(r, e))
                r = e
        return matches

    def collapse(self):
        n = self.size
        for c in range(n):
            col = [self.grid[r][c] for r in range(n) if self.grid[r][c] is not None]
            col = [self.rng.randrange(self.types) for _ in range(n - len(col))] + col
            for r in range(n):
                self.grid[r][c] = col[r]

    def find_move(self):
        n = self.size
        for r in range(n):
            for c in range(n):
                for dr, dc in ((0, 1), (1, 0)):
                    a, b = (r, c), (r + dr, c + dc)
                    if b[0] < n and b[1] < n:
                        self.swap(a, b)
                        ok = bool(self.find_matches())
                        self.swap(a, b)
                        if ok:
                            return a, b
        return None


class Game:
    MOVES = 20
    TARGET = 3000

    def __init__(self, size=8, types=6, seed=None):
        self.board = Board(size, types, seed)
        self.score = 0
        self.moves_left = self.MOVES
        self.over = False

    def move(self, a, b):
        n = self.board.size
        if not all(0 <= v < n for v in a + b):
            return "Move is out of bounds."
        if abs(a[0] - b[0]) + abs(a[1] - b[1]) != 1:
            return "Candies must be adjacent."
        self.board.swap(a, b)
        if not self.board.find_matches():
            self.board.swap(a, b)
            return "No match made - swap reverted."
        self.moves_left -= 1
        chain, gained = 0, 0
        while True:
            m = self.board.find_matches()
            if not m:
                break
            chain += 1
            pts = len(m) * 60 * chain
            gained += pts
            for r, c in m:
                self.board.grid[r][c] = None
            self.board.collapse()
        self.score += gained
        msg = f"Chain x{chain}! +{gained} points."
        if not self.board.find_move():
            self.board.reset()
            msg += " No moves left on board - reshuffled."
        if self.score >= self.TARGET or self.moves_left <= 0:
            self.over = True
        return msg