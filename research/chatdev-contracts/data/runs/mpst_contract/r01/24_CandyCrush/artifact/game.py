"""Core match-3 game logic: board, swaps, matches, gravity, cascades, scoring."""
import random

COLORS = "ROYGBP"
SYMBOLS = {
    "R": ("Red", "\033[91m"),
    "O": ("Orange", "\033[38;5;208m"),
    "Y": ("Yellow", "\033[93m"),
    "G": ("Green", "\033[92m"),
    "B": ("Blue", "\033[94m"),
    "P": ("Purple", "\033[95m"),
}
TARGET_SCORE = 1500
DEFAULT_MOVES = 20


class Match3Game:
    def __init__(self, rows=8, cols=8, moves=DEFAULT_MOVES, seed=None):
        self.rows = rows
        self.cols = cols
        self.moves_left = moves
        self.score = 0
        self.rng = random.Random(seed)
        self._fill_board()

    def _fill_board(self):
        while True:
            self.board = [[self.rng.choice(COLORS) for _ in range(self.cols)]
                          for _ in range(self.rows)]
            if not self.find_matches() and self.has_any_move():
                return

    def in_bounds(self, r, c):
        return 0 <= r < self.rows and 0 <= c < self.cols

    def find_matches(self):
        matches = set()
        for r in range(self.rows):
            run = 1
            for c in range(1, self.cols + 1):
                if c < self.cols and self.board[r][c] == self.board[r][c - 1]:
                    run += 1
                else:
                    if run >= 3:
                        matches.update((r, cc) for cc in range(c - run, c))
                    run = 1
        for c in range(self.cols):
            run = 1
            for r in range(1, self.rows + 1):
                if r < self.rows and self.board[r][c] == self.board[r - 1][c]:
                    run += 1
                else:
                    if run >= 3:
                        matches.update((rr, c) for rr in range(r - run, r))
                    run = 1
        return matches

    def swap(self, r1, c1, r2, c2):
        self.board[r1][c1], self.board[r2][c2] = self.board[r2][c2], self.board[r1][c1]

    def is_valid_move(self, r1, c1, r2, c2):
        if not (self.in_bounds(r1, c1) and self.in_bounds(r2, c2)):
            return False
        if abs(r1 - r2) + abs(c1 - c2) != 1:
            return False
        self.swap(r1, c1, r2, c2)
        ok = bool(self.find_matches())
        self.swap(r1, c1, r2, c2)
        return ok

    def resolve(self):
        """Clear matches, drop candies, refill; repeat for chain reactions."""
        total = 0
        cascade = 0
        while True:
            matches = self.find_matches()
            if not matches:
                return total, cascade
            cascade += 1
            total += len(matches) * 20 * cascade
            for r, c in matches:
                self.board[r][c] = None
            for c in range(self.cols):
                stack = [self.board[r][c] for r in range(self.rows - 1, -1, -1)
                         if self.board[r][c] is not None]
                for r in range(self.rows - 1, -1, -1):
                    self.board[r][c] = stack.pop(0) if stack else self.rng.choice(COLORS)

    def move(self, r1, c1, r2, c2):
        """Apply a swap if it forms a match. Returns (points, cascades, shuffled) or None."""
        if not self.is_valid_move(r1, c1, r2, c2):
            return None
        self.swap(r1, c1, r2, c2)
        points, cascades = self.resolve()
        self.score += points
        self.moves_left -= 1
        shuffled = False
        if not self.has_any_move():
            self.shuffle()
            shuffled = True
        return points, cascades, shuffled

    def has_any_move(self):
        for r in range(self.rows):
            for c in range(self.cols):
                for dr, dc in ((0, 1), (1, 0)):
                    if self.is_valid_move(r, c, r + dr, c + dc):
                        return True
        return False

    def shuffle(self):
        while True:
            flat = [self.rng.choice(COLORS) for _ in range(self.rows * self.cols)]
            self.board = [flat[i * self.cols:(i + 1) * self.cols] for i in range(self.rows)]
            if not self.find_matches() and self.has_any_move():
                return

    def over(self):
        return self.moves_left <= 0 or not self.has_any_move()