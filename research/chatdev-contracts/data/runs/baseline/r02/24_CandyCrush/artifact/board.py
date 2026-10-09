import random
import pygame
from settings import *
from candy import Candy, IDLE, SWAPPING, FALLING, CLEARING, SPAWNING, DEAD
class Board:
    def __init__(self):
        self.rows = GRID_ROWS
        self.cols = GRID_COLS
        self.grid = [[None] * self.cols for _ in range(self.rows)]
        self.chain = 0
        self.generate()
    def in_bounds(self, r, c):
        return 0 <= r < self.rows and 0 <= c < self.cols
    def get(self, r, c):
        if self.in_bounds(r, c):
            return self.grid[r][c]
        return None
    def creates_match_at(self, r, c, t):
        # horizontal run
        count = 1
        cc = c - 1
        while cc >= 0 and self.grid[r][cc] is not None and self.grid[r][cc].type == t:
            count += 1; cc -= 1
        cc = c + 1
        while cc < self.cols and self.grid[r][cc] is not None and self.grid[r][cc].type == t:
            count += 1; cc += 1
        if count >= 3:
            return True
        # vertical run
        count = 1
        rr = r - 1
        while rr >= 0 and self.grid[rr][c] is not None and self.grid[rr][c].type == t:
            count += 1; rr -= 1
        rr = r + 1
        while rr < self.rows and self.grid[rr][c] is not None and self.grid[rr][c].type == t:
            count += 1; rr += 1
        return count >= 3