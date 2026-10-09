'''
Candy entity: visual + animation state for a single board piece.
'''
import math
import pygame
from constants import ...
class Candy:
    def __init__(self, candy_type, row, col):
        self.type = candy_type
        self.row = row
        self.col = col
        self.x = ...  # pixel center x
        self.y = ...
        self.scale = 1.0
        self.alpha = 255
        self.selected = False
        self.offset_phase = random for wobble? maybe not
    @property
    def target_x(self): return BOARD_X + self.col * CELL_SIZE + CELL_SIZE // 2
    @property
    def target_y(self): return BOARD_Y + self.row * CELL_SIZE + CELL_SIZE // 2
    def set_position(self, row, col): ...
    def snap_to_target(self): ...
    def is_at_target(self): ...
    def draw(self, surface): draws shape with scale/alpha