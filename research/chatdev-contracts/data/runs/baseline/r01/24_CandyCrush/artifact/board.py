'''Game board: grid of candies with match detection, swapping, gravity, refill and deadlock checks.'''
import random
import config
from candy import Candy
class Board:
    def __init__(self, rows, cols, num_types):
        self.rows = rows
        self.cols = cols
        self.num_types = num_types
        self.grid = [[None] * cols for _ in range(rows)]
        self.fill_initial()
    def in_bounds(self, r, c):
        return 0 <= r < self.rows and 0 <= c < self.cols
    def get(self, r, c):
        if self.in_bounds(r, c):
            return self.grid[r][c]
        return None
    def fill_initial(self):
        for attempt in range(100):
            for r in range(self.rows):
                for c in range(self.cols):
                    self.grid[r][c] = Candy(random.randrange(self.num_types), r, c)
            self.remove_initial_matches()
            if self.find_possible_moves():
                return
        # fallback: accept last state (extremely unlikely)
    def remove_initial_matches(self):
        # Re-roll cells that participate in horizontal/vertical runs of 3+
        for r in range(self.rows):
            for c in range(self.cols):
                while True:
                    t = self.grid[r][c].type_id
                    horiz = 1
                    cc = c - 1
                    while cc >= 0 and self.grid[r][cc].type_id == t:
                        horiz += 1
                        cc -= 1
                    cc = c + 1
                    while cc < self.cols and self.grid[r][cc].type_id == t:
                        horiz += 1
                        cc += 1
                    vert = 1
                    rr = r - 1
                    while rr >= 0 and self.grid[rr][c].type_id == t:
                        vert += 1
                        rr -= 1
                    rr = r + 1
                    while rr < self.rows and self.grid[rr][c].type_id == t:
                        vert += 1
                        rr += 1
                    if horiz >= 3 or vert >= 3:
                        self.grid[r][c].type_id = random.randrange(self.num_types)
                    else:
                        break