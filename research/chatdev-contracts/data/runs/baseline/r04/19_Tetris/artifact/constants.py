'''
constants.py
Global configuration constants for the Tetris game: board dimensions,
cell size, colors, scoring values, and speed progression settings.
'''
# Screen / board configuration
CELL_SIZE = 30
BOARD_WIDTH = 10   # number of cells horizontally
BOARD_HEIGHT = 20  # number of cells vertically
# Side panel width for score / next piece display
PANEL_WIDTH = 260
# Screen dimensions (board + panel + margins)
MARGIN = 20
SCREEN_WIDTH = MARGIN * 2 + BOARD_WIDTH * CELL_SIZE + PANEL_WIDTH
SCREEN_HEIGHT = MARGIN * 2 + BOARD_HEIGHT * CELL_SIZE
# Frames per second for the main loop
FPS = 60
# Colors (R, G, B)
COLOR_BACKGROUND = (18, 18, 26)
COLOR_BOARD = (24, 24, 34)
COLOR_GRID = (40, 40, 52)
COLOR_BORDER = (90, 90, 110)
COLOR_TEXT = (230, 230, 240)
COLOR_GHOST = (120, 120, 140)
# Tetromino colors
COLORS = {
    'I': (0, 200, 220),
    'O': (230, 200, 0),
    'T': (170, 60, 200),
    'S': (0, 200, 80),
    'Z': (220, 60, 60),
    'J': (60, 90, 220),
    'L': (230, 140, 0),
}
# Scoring
SCORE_SINGLE = 100
SCORE_DOUBLE = 300
SCORE_TRIPLE = 500
SCORE_TETRIS = 800
SCORE_SOFT_DROP = 1    # per cell
SCORE_HARD_DROP = 2    # per cell
LINES_PER_LEVEL = 10
# Gravity: base seconds per drop, multiplied by a speed factor per level
BASE_DROP_INTERVAL = 0.8   # seconds at level 1
SPEED_FACTOR = 0.85        # interval multiplier applied per level
MIN_DROP_INTERVAL = 0.05   # fastest allowed drop interval
# Key auto-repeat (DAS: Delayed Auto Shift)
DAS_DELAY = 0.17     # initial delay before auto-repeat starts
DAS_INTERVAL = 0.05  # seconds between repeats