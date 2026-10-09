'''
constants.py
Central configuration for the 2048 game: board dimensions, window layout,
color palette (classic 2048 theme), fonts and timing constants.
'''
# ---------------------------------------------------------------------------
# Board / layout
# ---------------------------------------------------------------------------
GRID_SIZE = 4          # 4x4 playing grid
CELL_SIZE = 100        # pixel size of a single tile cell
CELL_GAP = 10          # pixel gap between cells
GRID_LEFT = 20         # left margin of the grid inside the window
GRID_TOP = 170         # top offset of the grid (below the header/score area)
# Derived window dimensions
WINDOW_WIDTH = GRID_LEFT * 2 + GRID_SIZE * CELL_SIZE + (GRID_SIZE + 1) * CELL_GAP
WINDOW_HEIGHT = GRID_TOP + GRID_SIZE * CELL_SIZE + (GRID_SIZE + 1) * CELL_GAP + 20
# ---------------------------------------------------------------------------
# Timing
# ---------------------------------------------------------------------------
FPS = 60
# ---------------------------------------------------------------------------
# Colors (R, G, B)
# ---------------------------------------------------------------------------
COLOR_BACKGROUND = (187, 173, 160)     # window background
COLOR_GRID_EMPTY = (205, 193, 180)     # empty cell background
COLOR_TEXT_DARK = (119, 110, 101)      # dark text (title, small tiles)
COLOR_TEXT_LIGHT = (249, 246, 242)     # light text (large tiles)
COLOR_SCORE_BOX = (187, 173, 160)      # score panel boxes
COLOR_STAT_BOX = COLOR_SCORE_BOX       # alias kept for backward compatibility
COLOR_OVERLAY = (238, 228, 218, 150)   # translucent game-over overlay
COLOR_OVERLAY_TEXT = (119, 110, 101)
COLOR_BANNER = (237, 194, 46)          # "2048 reached" banner
# Tile colors keyed by tile value (classic 2048 palette).
# Values above 2048 fall back to TILE_COLOR_SUPER.
TILE_COLORS = {
    2:    (238, 228, 218),
    4:    (237, 224, 200),
    8:    (242, 177, 121),
    16:   (245, 149, 99),
    32:   (246, 124, 95),
    64:   (246, 94, 59),
    128:  (237, 207, 114),
    256:  (237, 204, 97),
    512:  (237, 200, 80),
    1024: (237, 197, 63),
    2048: (237, 194, 46),
}
TILE_COLOR_SUPER = (60, 58, 50)        # tiles above 2048
# Tiles rendered with dark text on light background
DARK_TEXT_TILES = {2, 4}
# ---------------------------------------------------------------------------
# Fonts
# ---------------------------------------------------------------------------
FONT_NAME = "arial"
FONT_SIZE_TITLE = 48
FONT_SIZE_TILE_LARGE = 44
FONT_SIZE_TILE_MEDIUM = 36
FONT_SIZE_TILE_SMALL = 28
FONT_SIZE_TILE_TINY = 22
FONT_SIZE_SCORE_LABEL = 14
FONT_SIZE_SCORE_VALUE = 24
FONT_SIZE_HINT = 16
FONT_SIZE_OVERLAY = 40
FONT_SIZE_OVERLAY_SUB = 20