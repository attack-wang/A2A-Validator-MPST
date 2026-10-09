'''Game board: grid of candies, match detection, swaps, gravity, cascades.'''
import random
import pygame
import settings as S
from candy import Candy
class Board:
    IDLE = 'idle'
    SWAPPING = 'swapping'
    SWAP_BACK = 'swap_back'
    CLEARING = 'clearing'
    FALLING = 'falling'
    def __init__(self):
        self.grid = [[None] * S.GRID_SIZE for _ in range(S.GRID_SIZE)]
        self.state = Board.IDLE
        self.cascade = 0
        self.last_swap = None  # (pos1, pos2) of the player's swap
        self.clearing = []  # candies currently animating out
        self.generate_initial()
    # --- setup -------------------------------------------------
    def generate_initial(self):
        while True:
            for y in range(S.GRID_SIZE):
                for x in range(S.GRID_SIZE):
                    self.grid[y][x] = Candy(random.randrange(S.CANDY_TYPES), x, y)
            # remove initial matches by re-rolling
            if not self.find_matches():
                break
        if not self.has_valid_moves():
            self.shuffle_types()
    ...