'''
board.py
Game board: grid of candies, match detection, gravity, refilling,
shuffling and hint search.
'''
import random
import config
from candy import Candy
class Board:
    def __init__(self, rng=None):
        self.rng = rng if rng is not None else random
        self.grid = [[None] * config.GRID_SIZE for _ in range(config.GRID_SIZE)]
        self._fill_initial()
    # --- construction helpers -------------------------------------------------
    def _fill_initial(self):
        """Fill the grid avoiding pre-existing matches; guarantee a valid move."""
        n = config.GRID_SIZE
        for r in range(n):
            for c in range(n):
                while True:
                    t = self.rng.randrange(config.NUM_CANDY_TYPES)
                    candy = Candy(t, r, c)
                    self.grid[r][c] = candy
                    if not self._creates_match_at(r, c):
                        break
                    self.grid[r][c] = None
        if not self.has_possible_moves():
            self.shuffle()
    def _creates_match_at(self, row, col):
        """True if the candy at (row, col) forms a run of 3+ with left/up neighbors."""
        t = self.grid[row][col]
        if t is None:
            return False
        # check left two
        if col >= 2:
            a, b = self.grid[row][col - 1], self.grid[row][col - 2]
            if a is not None and b is not None and a.type == t.type and b.type == t.type:
                return True
        # check up two
        if row >= 2:
            a, b = self.grid[row - 1][col], self.grid[row - 2][col]
            if a is not None and b is not None and a.type == t.type and b.type == t.type:
                return True
        return False