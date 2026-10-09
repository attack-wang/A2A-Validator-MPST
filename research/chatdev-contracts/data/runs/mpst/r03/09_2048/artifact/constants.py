'''
constants.py
This module defines all the shared constants used across the 2048 game,
including grid dimensions, window layout metrics, the color palette for
tiles and background, and timing settings.
'''
# Grid configuration
GRID_SIZE = 4  # The game is played on a 4x4 grid
# Window layout configuration
WINDOW_WIDTH = 600
WINDOW_HEIGHT = 700  # Extra vertical space for the score panel
CELL_SIZE = 120
CELL_GAP = 12
GRID_TOP = 160  # Y offset where the grid starts (below the score panel)
GRID_LEFT = (WINDOW_WIDTH - (GRID_SIZE * CELL_SIZE + (GRID_SIZE + 1) * CELL_GAP)) // 2
# Timing configuration
FPS = 60
# Colors (R, G, B)
COLOR_BACKGROUND = (250, 248, 239)
COLOR_GRID_BACKGROUND = (187, 173, 160)
COLOR_EMPTY_CELL = (205, 193, 180)
COLOR_TEXT_DARK = (119, 110, 101)
COLOR_TEXT_LIGHT = (249, 246, 242)
COLOR_SCORE_BOX = (187, 173, 160)
COLOR_GAME_OVER_OVERLAY = (250, 248, 239, 150)
# Tile colors: value -> (background_color, text_color)
TILE_COLORS = {
    2:    ((238, 228, 218), COLOR_TEXT_DARK),
    4:    ((237, 224, 200), COLOR_TEXT_DARK),
    8:    ((242, 177, 121), COLOR_TEXT_LIGHT),
    16:   ((245, 149, 99),  COLOR_TEXT_LIGHT),
    32:   ((246, 124, 95),  COLOR_TEXT_LIGHT),
    64:   ((246, 94, 59),   COLOR_TEXT_LIGHT),
    128:  ((237, 207, 114), COLOR_TEXT_LIGHT),
    256:  ((237, 204, 97),  COLOR_TEXT_LIGHT),
    512:  ((237, 200, 80),  COLOR_TEXT_LIGHT),
    1024: ((237, 197, 63),  COLOR_TEXT_LIGHT),
    2048: ((237, 194, 46),  COLOR_TEXT_LIGHT),
}
# Fallback color for tiles beyond 2048
TILE_COLOR_SUPER = ((60, 58, 50), COLOR_TEXT_LIGHT)
# Font sizes
FONT_SIZE_TITLE = 48
FONT_SIZE_SCORE = 22
FONT_SIZE_TILE_LARGE = 48
FONT_SIZE_TILE_MEDIUM = 40
FONT_SIZE_TILE_SMALL = 32
FONT_SIZE_MESSAGE = 40