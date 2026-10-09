'''Board module: grid management, match detection, gravity/refill, swap validation, shuffling.'''
import random
import config
from candy import Candy
class Board:
    def __init__(self, rows=None, cols=None, num_types=None):
        self.rows = rows if rows is not None else config.GRID_ROWS
        self.cols = cols if cols is not None else config.GRID_COLS
        self.num_types = num_types if num_types is not None else config.NUM_CANDY_TYPES
        self.fill_initial()
    def in_bounds(self, row, col):
        return 0 <= row < self.rows and 0 <= col < self.cols
    def get(self, row, col):
        if self.in_bounds(row, col):
            return self.grid[row][col]
        return None
    def set(self, row, col, candy):
        self.grid[row][col] = candy
    def _random_type(self):
        return random.randrange(self.num_types)
    def _random_type_no_match(self, row, col):
        while True:
            t = self._random_type()
            if (col >= 2 and self.grid[row][col - 1] is not None
                    and self.grid[row][col - 2] is not None
                    and self.grid[row][col - 1].type == t
                    and self.grid[row][col - 2].type == t):
                continue
            if (row >= 2 and self.grid[row - 1][col] is not None
                    and self.grid[row - 2][col] is not None
                    and self.grid[row - 1][col].type == t
                    and self.grid[row - 2][col].type == t):
                continue
            return t
    def fill_initial(self):
        """Create a fresh board with no pre-existing matches and at least one possible move."""
        while True:
            self.grid = [[None] * self.cols for _ in range(self.rows)]
            for r in range(self.rows):
                for c in range(self.cols):
                    self.grid[r][c] = Candy(self._random_type_no_match(r, c), r, c)
            if self.find_possible_move() is not None:
                break
    def find_matches(self):
        """Return (set_of_positions, list_of_run_lengths). Positions are (row, col) tuples."""
        matches = set()
        run_lengths = []
        # horizontal
        for r in range(self.rows):
            run_start = 0
            for c in range(1, self.cols + 1):
                prev = self.get(r, c - 1)
                cur = self.get(r, c) if c < self.cols else None
                same = cur is not None and prev is not None and cur.type == prev.type
                if c == self.cols or not same:
                    run_len = c - run_start
                    if run_len >= 3 and prev is not None:
                        run_lengths.append(run_len)
                        for cc in range(run_start, c):
                            matches.add((r, cc))
                    run_start = c
        # vertical
        for c in range(self.cols):
            run_start = 0
            for r in range(1, self.rows + 1):
                prev = self.get(r - 1, c)
                cur = self.get(r, c) if r < self.rows else None
                same = cur is not None and prev is not None and cur.type == prev.type
                if r == self.rows or not same:
                    run_len = r - run_start
                    if run_len >= 3 and prev is not None:
                        run_lengths.append(run_len)
                        for rr in range(run_start, r):
                            matches.add((rr, c))
                    run_start = r
        return matches, run_lengths