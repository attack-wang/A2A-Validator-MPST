"""
constants.py
Central configuration for the Tetris game: board dimensions, cell size,
colors, tetromino shape matrices, scoring rules, and speed progression.
"""
# Board dimensions (standard Tetris playfield)
BOARD_WIDTH = 10
BOARD_HEIGHT = 20
# Rendering geometry
CELL_SIZE = 30
BOARD_OFFSET_X = 40
BOARD_OFFSET_Y = 40
SIDEBAR_WIDTH = 210
WINDOW_WIDTH = BOARD_OFFSET_X * 2 + BOARD_WIDTH * CELL_SIZE + SIDEBAR_WIDTH
WINDOW_HEIGHT = BOARD_OFFSET_Y * 2 + BOARD_HEIGHT * CELL_SIZE
FPS = 60
# Colors
COLOR_BACKGROUND = (18, 18, 24)
COLOR_BOARD = (10, 10, 14)
COLOR_GRID = (40, 40, 52)
COLOR_BORDER = (90, 90, 110)
COLOR_TEXT = (235, 235, 235)
COLOR_TEXT_DIM = (150, 150, 160)
SHAPE_COLORS = {
    'I': (0, 200, 220),
    'O': (230, 200, 0),
    'T': (170, 60, 220),
    'S': (60, 200, 60),
    'Z': (220, 60, 60),
    'J': (60, 90, 220),
    'L': (230, 140, 30),
}
SHAPES = {
    'I': [[0, 0, 0, 0], [1, 1, 1, 1], [0, 0, 0, 0], [0, 0, 0, 0]],
    'O': [[1, 1], [1, 1]],
    'T': [[0, 1, 0], [1, 1, 1], [0, 0, 0]],
    'S': [[0, 1, 1], [1, 1, 0], [0, 0, 0]],
    'Z': [[1, 1, 0], [0, 1, 1], [0, 0, 0]],
    'J': [[1, 0, 0], [1, 1, 1], [0, 0, 0]],
    'L': [[0, 0, 1], [1, 1, 1], [0, 0, 0]],
}
# Scoring
LINE_SCORES = {1: 100, 2: 300, 3: 500, 4: 800}
SOFT_DROP_POINTS = 1
HARD_DROP_POINTS = 2
LINES_PER_LEVEL = 10
# Gravity / speed progression
BASE_DROP_INTERVAL = 0.8
MIN_DROP_INTERVAL = 0.05
SPEED_MULTIPLIER = 0.82
def get_drop_interval(level):
    """Return the automatic drop interval (seconds) for the given level."""
    interval = BASE_DROP_INTERVAL * (SPEED_MULTIPLIER ** (level - 1))
    return max(MIN_DROP_INTERVAL, interval)