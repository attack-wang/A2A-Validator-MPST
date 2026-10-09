"""Board: grid state, match detection, gravity/refill, shuffle, rendering."""
import random
import pygame
from settings import (BOARD_X, BOARD_Y, CELL_SIZE, GRID_SIZE, NUM_CANDY_TYPES,
                      COLOR_BOARD_BG, COLOR_CELL)
from candy import Candy
class Board:
    """The match-3 board: grid state, match detection, gravity, refill, shuffle."""
    def __init__(self):
        self.rows = GRID_SIZE
        self.cols = GRID_SIZE
        self.grid = [[None for _ in range(self.cols)] for _ in range(self.rows)]
        self.fill_initial()
    # ---------- setup ----------
    def fill_initial(self):
        """Fill the board with random candies that create no immediate matches
        and guarantee at least one valid move."""
        while True:
            self.grid = [[None for _ in range(self.cols)] for _ in range(self.rows)]
            for y in range(self.rows):
                for x in range(self.cols):
                    while True:
                        t = random.randrange(NUM_CANDY_TYPES)
                        if x >= 2 and self.grid[y][x - 1] is not None and self.grid[y][x - 2] is not None \
                                and self.grid[y][x - 1].candy_type == t and self.grid[y][x - 2].candy_type == t:
                            continue
                        if y >= 2 and self.grid[y - 1][x] is not None and self.grid[y - 2][x] is not None \
                                and self.grid[y - 1][x].candy_type == t and self.grid[y - 2][x].candy_type == t:
                            continue
                        c = Candy(t, x, y)
                        c.sync_pixel_to_grid(BOARD_X, BOARD_Y)
                        self.grid[y][x] = c
                        break
            if self.find_valid_move() is not None:
                return