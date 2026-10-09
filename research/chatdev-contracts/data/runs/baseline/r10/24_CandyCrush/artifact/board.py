"""Board model: grid of candies, match detection, gravity, move generation."""
import random
from config import GRID_SIZE, NUM_CANDY_TYPES
from candy import Candy
class Board:
    def __init__(self, rows=GRID_SIZE, cols=GRID_SIZE, rng=None):
        self.rows = rows
        self.cols = cols
        self.rng = rng or random.Random()
        self.grid = [[None] * cols for _ in range(rows)]
        self.fill_initial()
    def in_bounds(self, r, c):
        return 0 <= r < self.rows and 0 <= c < self.cols
    def candy_at(self, r, c):
        if self.in_bounds(r, c):
            return self.grid[r][c]
        return None
    def generate_type(self):
        return self.rng.randrange(NUM_CANDY_TYPES)
    def fill_initial(self):
        """Fill board with no pre-existing matches and at least one move."""
        while True:
            self.grid = [[None] * self.cols for _ in range(self.rows)]
            for r in range(self.rows):
                for c in range(self.cols):
                    forbidden = set()
                    if c >= 2 and self.grid[r][c-1].type == self.grid[r][c-2].type:
                        forbidden.add(self.grid[r][c-1].type)
                    if r >= 2 and self.grid[r-1][c].type == self.grid[r-2][c].type:
                        forbidden.add(self.grid[r-1][c].type)
                    choices = [t for t in range(NUM_CANDY_TYPES) if t not in forbidden]
                    t = self.rng.choice(choices)
                    self.grid[r][c] = Candy(t, r, c)
            if not self.find_matches() and self.find_possible_moves():
                break
    def find_matches(self):
        """Return set of (r, c) cells belonging to any horizontal/vertical run >= 3."""
        matches = set()
        for r in range(self.rows):
            run_start = 0
            for c in range(1, self.cols + 1):
                if (c < self.cols and self.grid[r][c] is not None
                        and self.grid[r][c].type == self.grid[r][run_start].type):
                    continue
                # run ends at c-1
                if c - run_start >= 3 and self.grid[r][run_start] is not None:
                    for cc in range(run_start, c):
                        matches.add((r, cc))
                run_start = c
        # same for columns
        for c in range(self.cols):
            run_start = 0
            for r in range(1, self.rows + 1):
                if (r < self.rows and self.grid[r][c] is not None
                        and self.grid[r][c].type == self.grid[run_start][c].type):
                    continue
                if r - run_start >= 3 and self.grid[run_start][c] is not None:
                    for rr in range(run_start, r):
                        matches.add((rr, c))
                run_start = r
        return matches