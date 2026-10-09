"""
constants.py
Central configuration for the 2048 game: window dimensions, layout metrics,
color palette, animation timings, and font sizes.
"""
# --- Window layout -------------------------------------------------------
CELL_SIZE = 110          # Pixel size of a single tile cell
CELL_GAP = 12            # Pixel gap between cells
GRID_MARGIN = 12         # Margin around the 4x4 grid
HEADER_HEIGHT = 110      # Height of the header area (title + score boxes)
GRID_COUNT = 4
GRID_PIXELS = GRID_COUNT * CELL_SIZE + (GRID_COUNT + 1) * CELL_GAP  # 4*110+5*12 = 500
WINDOW_WIDTH = GRID_PIXELS + 2 * GRID_MARGIN          # 524
WINDOW_HEIGHT = HEADER_HEIGHT + GRID_PIXELS + 2 * GRID_MARGIN  # 634
FPS = 60
# --- Animation timings (milliseconds) ------------------------------------
MOVE_DURATION = 110      # Slide animation duration
POP_DURATION = 90        # Scale "pop" duration for merged/new tiles
# --- Colors --------------------------------------------------------------
COLOR_BACKGROUND = (250, 248, 239)      # #faf8ef
COLOR_GRID_BACKGROUND = (187, 173, 160) # #bbada0
COLOR_CELL_EMPTY = (205, 193, 180)      # #cdc1b4
COLOR_TEXT_DARK = (119, 110, 101)       # #776e65
COLOR_TEXT_LIGHT = (249, 246, 242)      # #f9f6f2
COLOR_OVERLAY = (250, 248, 239)         # overlay base, used with alpha
# (fill_color, text_color) per tile value; values above 2048 use SUPER entry
TILE_COLORS = {
    2:    ((238, 228, 218), (119, 110, 101)),
    4:    ((237, 224, 200), (119, 110, 101)),
    8:    ((242, 177, 121), (249, 246, 242)),
    16:   ((245, 149, 99),  (249, 246, 242)),
    32:   ((246, 124, 95),  (249, 246, 242)),
    64:   ((246, 94, 59),   (249, 246, 242)),
    128:  ((237, 207, 114), (249, 246, 242)),
    256:  ((237, 204, 97),  (249, 246, 242)),
    512:  ((237, 200, 80),  (249, 246, 242)),
    1024: ((237, 197, 63),  (249, 246, 242)),
    2048: ((237, 194, 46),  (249, 246, 242)),
}
TILE_COLOR_SUPER = ((60, 58, 50), (249, 246, 242))
# --- Fonts ---------------------------------------------------------------
FONT_NAME = "arial"
FONT_SIZE_TITLE = 56
FONT_SIZE_SCORE_LABEL = 16
FONT_SIZE_SCORE_VALUE = 26
FONT_SIZE_TILE = {1: 52, 2: 48, 3: 40, 4: 32, 5: 26}  # keyed by digit count
FONT_SIZE_MESSAGE = 44
FONT_SIZE_SUB_MESSAGE = 22
FONT_SIZE_HINT = 18