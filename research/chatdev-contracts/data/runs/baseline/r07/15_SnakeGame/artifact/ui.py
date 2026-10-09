'''
ui.py
Rendering helpers: fonts, text, grid, HUD bar, pause/game-over overlays
and menu button geometry.
'''
import pygame
from settings import (
    WINDOW_WIDTH, WINDOW_HEIGHT, HUD_HEIGHT, BOARD_HEIGHT,
    GRID_SIZE, GRID_WIDTH, GRID_HEIGHT,
    BLACK, DARK_GRAY, GRID_LINE, GRAY, WHITE, RED, YELLOW,
    DIFFICULTY_LEVELS, DIFFICULTY_ORDER,
)
_font_cache = {}
def get_font(size, bold=True):
    '''Return a cached pygame font, trying preferred monospace fonts first.'''
    key = (size, bold)
    if key not in _font_cache:
        try:
            font = pygame.font.SysFont(",".join(FONT_CANDIDATES), size, bold=bold)
        except Exception:
            font = pygame.font.Font(None, size + 10)
        _font_cache[key] = font
    return _font_cache[key]