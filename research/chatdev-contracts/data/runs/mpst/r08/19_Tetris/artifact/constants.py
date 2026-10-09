'''
constants.py
Central configuration module for the Tetris game.
Defines board dimensions, cell size, refresh interval, tetromino shape
matrices, their associated colors, scoring values, and level-based speed
settings. Imported by every other module so that gameplay tuning only
needs to happen in one place.
'''
# Board dimensions (in cells)
BOARD_WIDTH = 10
BOARD_HEIGHT = 20
# Rendering
CELL_SIZE = 32
SIDEBAR_WIDTH = 220
SCREEN_WIDTH = BOARD_WIDTH * CELL_SIZE + SIDEBAR_WIDTH
SCREEN_HEIGHT = BOARD_HEIGHT * CELL_SIZE
FRAME_INTERVAL_MS = 50   # logic/refresh tick (20 fps logic, smooth enough)
# Window / UI text
WINDOW_TITLE = "Tetris"
# Colors (R, G, B) -> converted to "#rrggbb" hex strings for tkinter
def _hex(rgb):
    return "#{:02x}{:02x}{:02x}".format(*rgb)
COLOR_BACKGROUND = _hex((18, 18, 24))
COLOR_GRID = _hex((40, 40, 48))
COLOR_BORDER = _hex((90, 90, 110))
COLOR_TEXT = _hex((230, 230, 235))
COLOR_TEXT_DIM = _hex((150, 150, 160))
COLOR_OVERLAY = _hex((10, 10, 14))