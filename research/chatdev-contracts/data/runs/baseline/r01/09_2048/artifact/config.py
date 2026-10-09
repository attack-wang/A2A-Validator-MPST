'''
Configuration constants for the 2048 game: window layout, colors, fonts,
and gameplay parameters.
'''
# ----------------------------------------------------------------------
# Window / layout (pixels)
# ----------------------------------------------------------------------
WINDOW_WIDTH = 500
WINDOW_HEIGHT = 640
FPS = 60
GRID_SIZE = 4          # 4x4 board
CELL_SIZE = 100        # side length of one tile cell
CELL_GAP = 12          # gap between cells
GRID_PADDING = 12      # inner padding of the grid background
GRID_LEFT = 20         # x position of the grid background
GRID_TOP = 150         # y position of the grid background (below header)
GRID_PIXELS = GRID_SIZE * CELL_SIZE + (GRID_SIZE + 1) * CELL_GAP  # 460
# ----------------------------------------------------------------------
# Gameplay parameters
# ----------------------------------------------------------------------
SPAWN_PROBABILITY_FOUR = 0.1   # chance a new tile is a 4 instead of a 2
TARGET_TILE = 2048             # tile that triggers the "you win" banner
# ----------------------------------------------------------------------
# Colors (R, G, B) - classic 2048 palette
# ----------------------------------------------------------------------
COLOR_BACKGROUND = (250, 248, 239)
COLOR_GRID_BG = (187, 173, 160)
COLOR_CELL_EMPTY = (205, 193, 180)
COLOR_TEXT_DARK = (119, 110, 101)
COLOR_TEXT_LIGHT = (249, 246, 242)
COLOR_OVERLAY = (238, 228, 218, 150)   # RGBA for the game-over overlay
COLOR_WIN_BANNER = (237, 194, 46)
# Tile background colors by value; values beyond 2048 use TILE_COLOR_DEFAULT
TILE_COLORS = {
    2: (238, 228, 218),
    4: (237, 224, 200),
    8: (242, 177, 121),
    16: (245, 149, 99),
    32: (246, 124, 95),
    64: (246, 94, 59),
    128: (237, 207, 114),
    256: (237, 204, 97),
    512: (237, 200, 80),
    1024: (237, 197, 63),
    2048: (237, 194, 46),
}
TILE_COLOR_DEFAULT = (60, 58, 50)
# ----------------------------------------------------------------------
# Font sizes
# ----------------------------------------------------------------------
FONT_SIZE_TITLE = 48
FONT_SIZE_SCORE_LABEL = 16
FONT_SIZE_SCORE_VALUE = 30
FONT_SIZE_BANNER = 18
FONT_SIZE_MESSAGE = 44
FONT_SIZE_HINT = 18