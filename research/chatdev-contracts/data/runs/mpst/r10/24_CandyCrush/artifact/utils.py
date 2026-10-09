'''Utility helpers shared across the match-3 game modules.'''
import config
def grid_to_pixel(row, col):
    """Return the center pixel coordinates (x, y) of a grid cell."""
    x = config.BOARD_X + col * config.CELL_SIZE + config.CELL_SIZE // 2
    y = config.BOARD_Y + row * config.CELL_SIZE + config.CELL_SIZE // 2
    return x, y
def pixel_to_grid(px, py):
    """Return the (row, col) grid coordinates for a pixel position, or None."""
    col = (px - config.BOARD_X) // config.CELL_SIZE
    row = (py - config.BOARD_Y) // config.CELL_SIZE
    if 0 <= row < config.ROWS and 0 <= col < config.COLS:
        return int(row), int(col)
    return None
def lerp(a, b, t):
    """Linear interpolation between a and b by factor t."""
    return a + (b - a) * t
def clamp(value, low, high):
    """Clamp value into the inclusive range [low, high]."""
    return max(low, min(high, value))