'''
Board model: grid of candies, match detection, gravity, refill, shuffling.
'''
import random
import settings
from candy import Candy
class Board:
    def __init__(self, rows=settings.GRID_SIZE, cols=settings.GRID_SIZE):
        self.rows = rows
        self.cols = cols
        self.grid = [[None for _ in range(cols)] for _ in range(rows)]
        self.fill_initial()
    # --- setup ---
    def fill_initial(self):
        while True:
            for r in range(self.rows):
                for c in range(self.cols):
                    self.grid[r][c] = self._random_candy_no_match(r, c)
            if self.has_valid_move():
                break
            # else regenerate (rare)
    def _random_candy_no_match(self, row, col):
        while True:
            t = random.randrange(settings.NUM_CANDY_TYPES)
            if not self._would_match_at(row, col, t):
                return Candy(t, row, col)
    def _would_match_at(self, row, col, type_id):
        # check horizontal run ending here
        count = 0
        c = col - 1
        while c >= 0 and self.grid[row][c] is not None and self.grid[row][c].type == type_id:
            count += 1; c -= 1
        if count >= 2: return True
        count = 0
        r = row - 1
        while r >= 0 and self.grid[r][col] is not None and self.grid[r][col].type == type_id:
            count += 1; r -= 1
        if count >= 2: return True
        return False