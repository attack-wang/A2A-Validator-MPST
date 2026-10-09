"""Board model: grid of candies, match detection, swapping, gravity, refill."""
import random
from settings import (ROWS, COLS, CELL_SIZE, BOARD_LEFT, BOARD_TOP,
                      NUM_CANDY_TYPES, SHUFFLE_SEARCH_LIMIT)
from candy import Candy
class Board:
    def __init__(self, rows=ROWS, cols=COLS, num_types=NUM_CANDY_TYPES):
        self.rows = rows
        self.cols = cols
        self.num_types = num_types
        self.grid = [[None] * cols for _ in range(rows)]
        self.generate_initial()
    # --- helpers ---
    def in_bounds(self, r, c):
        return 0 <= r < self.rows and 0 <= c < self.cols
    def get(self, r, c):
        if self.in_bounds(r, c):
            return self.grid[r][c]
        return None
    def cell_to_pixel(self, r, c):
        x = BOARD_LEFT + c * CELL_SIZE
        y = BOARD_TOP + r * CELL_SIZE
        return x, y
    def pixel_to_cell(self, px, py):
        c = (px - BOARD_LEFT) // CELL_SIZE
        r = (py - BOARD_TOP) // CELL_SIZE
        if self.in_bounds(r, c):
            return int(r), int(c)
        return None
    # --- generation ---
    def generate_initial(self):
        for _ in range(SHUFFLE_SEARCH_LIMIT // 100):  # hmm
            self._fill_no_matches()
            if self.find_possible_move() is not None:
                self._sync_positions()
                return
        # fallback: random fill (virtually never reached)
        ...