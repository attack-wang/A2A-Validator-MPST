"""Candy entity: grid position, animated pixel position, per-state animation."""
import pygame
from config import (CELL_SIZE, SWAP_DURATION, CLEAR_DURATION,
                    FALL_GRAVITY, FALL_MAX_SPEED, BOARD_TOP)
from graphics import get_candy_image
def pixel_pos(row, col):
    """Return the (px, py) center of the cell at (row, col)."""
    x = 20 + col * CELL_SIZE + CELL_SIZE // 2
    y = BOARD_TOP + row * CELL_SIZE + CELL_SIZE // 2
    return x, y