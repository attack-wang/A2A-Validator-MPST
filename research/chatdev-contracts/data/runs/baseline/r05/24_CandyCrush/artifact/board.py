import random
from constants import GRID_SIZE, NUM_CANDY_TYPES
from candy import Candy
class Board:
    def __init__(self, rows=GRID_SIZE, cols=GRID_SIZE):
        self.rows = rows
        self.cols = cols
        self.grid = [[None for _ in range(cols)] for _ in range(rows)]
        self.generate()
    def in_bounds(self, r, c): ...
    def candy_at(self, r, c): ...
    def are_adjacent(self, pos_a, pos_b): ...
    def generate(self):
        for _attempt in range(100):
            self._fill_without_matches()
            if self.has_valid_move():
                return
        # fallback: shuffle types randomly until valid (extremely unlikely to loop forever)
        while not self.has_valid_move():
            self._fill_without_matches()
    def _fill_without_matches(self):
        self.grid = [[None for _ in range(self.cols)] for _ in range(self.rows)]
        for r in range(self.rows):
            for c in range(self.cols):
                forbidden = set()
                # check two to the left
                if c >= 2:
                    t1 = self.grid[r][c-1]
                    t2 = self.grid[r][c-2]
                    if t1 and t2 and t1.type == t2.type:
                        forbidden.add(t1.type)
                if r >= 2:
                    t1 = self.grid[r-1][c]
                    t2 = self.grid[r-2][c]
                    if t1 and t2 and t1.type == t2.type:
                        forbidden.add(t1.type)
                choices = [t for t in range(NUM_CANDY_TYPES) if t not in forbidden]
                self.grid[r][c] = Candy(random.choice(choices))