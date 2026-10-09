'''
constants.py
Global configuration constants for the Tetris game.
'''
# Board dimensions (in cells)
BOARD_WIDTH = 10
BOARD_HEIGHT = 20
# Cell size in pixels
CELL_SIZE = 30
# Board pixel dimensions
BOARD_PIXEL_WIDTH = BOARD_WIDTH * CELL_SIZE
BOARD_PIXEL_HEIGHT = BOARD_HEIGHT * CELL_SIZE
# Sidebar dimensions
SIDEBAR_WIDTH = 220
SIDEBAR_PADDING = 10
# Window dimensions
WINDOW_WIDTH = BOARD_PIXEL_WIDTH + SIDEBAR_WIDTH
WINDOW_HEIGHT = BOARD_PIXEL_HEIGHT
# Frame rate
FPS = 60
# Colors (R, G, B)
COLOR_BG = (20, 20, 30)
COLOR_BOARD = (10, 10, 20)
COLOR_GRID = (40, 40, 55)
COLOR_BORDER = (120, 120, 140)
COLOR_TEXT = (230, 230, 230)
COLOR_GHOST = (90, 90, 110)
COLOR_GAME_OVER = (200, 40, 40)
# Tetromino colors
COLORS = {
    'I': (0, 200, 220),
    'O': (230, 200, 0),
    'T': (170, 60, 220),
    'S': (0, 200, 80),
    'Z': (230, 60, 60),
    'J': (60, 90, 230),
    'L': (240, 140, 0),
}
# Tetromino shape matrices
SHAPES = {
    'I': [[1, 1, 1, 1]],
    'O': [[1, 1], [1, 1]],
    'T': [[0, 1, 0], [1, 1, 1]],
    'S': [[0, 1, 1], [1, 1, 0]],
    'Z': [[1, 1, 0], [0, 1, 1]],
    'J': [[1, 0, 0], [1, 1, 1]],
    'L': [[0, 0, 1], [1, 1, 1]],
}
# Scoring per number of lines cleared at once
LINE_SCORES = {1: 100, 2: 300, 3: 500, 4: 800}
# Lines needed to advance to the next level
LINES_PER_LEVEL = 10
# Gravity timing (milliseconds) at level 1 and the fastest allowed
INITIAL_DROP_DELAY = 800
MIN_DROP_DELAY = 80
DROP_DELAY_STEP = 70  # reduction per level
# Soft drop speed multiplier
SOFT_DROP_DELAY = 50
# Preview area
PREVIEW_SIZE = 4 * CELL_SIZE