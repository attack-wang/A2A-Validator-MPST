import random
from collections import deque
from candy import Candy
from ui import CELL_SIZE, ROWS, COLS, NUM_CANDY_TYPES
class Board:
    def __init__(self, rows=ROWS, cols=COLS, num_types=NUM_CANDY_TYPES, rng=None):
        self.rows = rows
        self.cols = cols
        self.num_types = num_types
        self.rng = rng or random.Random()
        self.grid = [[None]*cols for _ in range(rows)]
        self.fill_initial()
    def random_candy(self):
        return Candy(self.rng.randrange(self.num_types))
    def in_bounds(self, r, c):
        return 0 <= r < self.rows and 0 <= c < self.cols
    def candy_at(self, r, c):
        if self.in_bounds(r, c):
            return self.grid[r][c]
        return None
    @staticmethod
    def are_adjacent(p1, p2):
        return abs(p1[0]-p2[0]) + abs(p1[1]-p2[1]) == 1
    def fill_initial(self):
        while True:
            for r in range(self.rows):
                for c in range(self.cols):
                    self.grid[r][c] = self.random_candy()
            self.remove_initial_matches()
            if self.has_valid_move():
                break
        # ensure no matches