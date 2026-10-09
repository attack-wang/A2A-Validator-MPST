'''
constants.py
Global configuration constants for the Tetris game, including board
dimensions, colors, scoring rules, speed progression and control keys.
'''
# Board dimensions
COLS = 10
ROWS = 20
CELL_SIZE = 30
# Window layout
SIDEBAR_WIDTH = 220
WINDOW_WIDTH = COLS * CELL_SIZE + SIDEBAR_WIDTH
WINDOW_HEIGHT = ROWS * CELL_SIZE
FPS = 60
# Colors
BLACK = (15, 15, 25)
WHITE = (240, 240, 240)
GRAY = (120, 120, 130)
GRID_COLOR = (40, 40, 55)
BORDER_COLOR = (90, 90, 110)
GHOST_COLOR = (70, 70, 90)
OVERLAY_COLOR = (10, 10, 20)
SHAPE_COLORS = {
    'I': (0, 230, 230),
    'O': (230, 230, 0),
    'T': (170, 0, 230),
    'S': (0, 230, 60),
    'Z': (230, 50, 50),
    'J': (60, 90, 230),
    'L': (230, 150, 30),
}
# Tetromino definitions
SHAPES = {
    'I': [[0, 0, 0, 0],
          [1, 1, 1, 1],
          [0, 0, 0, 0],
          [0, 0, 0, 0]],
    'O': [[1, 1],
          [1, 1]],
    'T': [[0, 1, 0],
          [1, 1, 1],
          [0, 0, 0]],
    'S': [[0, 1, 1],
          [1, 1, 0],
          [0, 0, 0]],
    'Z': [[1, 1, 0],
          [0, 1, 1],
          [0, 0, 0]],
    'J': [[1, 0, 0],
          [1, 1, 1],
          [0, 0, 0]],
    'L': [[0, 0, 1],
          [1, 1, 1],
          [0, 0, 0]],
}
# Scoring
LINE_SCORES = {1: 100, 2: 300, 3: 500, 4: 800}
SOFT_DROP_SCORE = 1
HARD_DROP_SCORE = 2
LINES_PER_LEVEL = 10
# Gravity
INITIAL_DROP_INTERVAL = 0.80
MIN_DROP_INTERVAL = 0.05
SPEED_FACTOR = 0.85