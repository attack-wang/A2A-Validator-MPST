'''
constants.py
Configuration constants for the Tetris game: board dimensions, colors,
tetromino shape definitions, scoring rules, speed progression, and key
auto-repeat (DAS) timing used by main.py.
'''
# Board dimensions
COLS = 10
ROWS = 20
CELL_SIZE = 30
# Window dimensions
SIDEBAR_WIDTH = 200
WINDOW_WIDTH = COLS * CELL_SIZE + SIDEBAR_WIDTH
WINDOW_HEIGHT = ROWS * CELL_SIZE
# Colors (R, G, B)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (128, 128, 128)
DARK_GRAY = (40, 40, 40)
GRID_LINE = (60, 60, 60)
# Tetromino colors
COLORS = {
    'I': (0, 240, 240),    # cyan
    'O': (240, 240, 0),    # yellow
    'T': (160, 0, 240),    # purple
    'S': (0, 240, 0),      # green
    'Z': (240, 0, 0),      # red
    'J': (0, 0, 240),      # blue
    'L': (240, 160, 0),    # orange
}
# Tetromino shape matrices (using 4x4 or smaller matrices)
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
SCORE_PER_LINE = {1: 100, 2: 300, 3: 500, 4: 800}
SOFT_DROP_POINTS = 1
HARD_DROP_POINTS = 2
# Speed
INITIAL_DROP_INTERVAL = 0.8  # seconds per drop at level 1
MIN_DROP_INTERVAL = 0.08
SPEED_FACTOR = 0.85  # multiply interval by this each level
LINES_PER_LEVEL = 10
# Key auto-repeat (Delayed Auto Shift) used by main.py
DAS_DELAY = 0.17  # seconds a key must be held before auto-repeat starts
DAS_RATE = 0.05   # seconds between auto-repeat moves once started
# Game
FPS = 60