'''
constants.py
Configuration constants for the Tetris game: dimensions, colors, shapes, speeds, and scoring.
'''
# --- Board dimensions ---
CELL_SIZE = 30          # pixels per grid cell
COLS = 10               # standard Tetris board width
ROWS = 20               # standard Tetris board height
# --- Window layout ---
SIDEBAR_WIDTH = 200
WINDOW_WIDTH = COLS * CELL_SIZE + SIDEBAR_WIDTH
WINDOW_HEIGHT = ROWS * CELL_SIZE
# --- Timing ---
FPS = 60
# --- Colors (R, G, B) ---
BLACK = (10, 10, 20)
WHITE = (240, 240, 240)
DARK_GRAY = (60, 60, 60)
GRID_LINE = (40, 40, 40)
SIDEBAR_BG = (25, 25, 35)
# --- Tetromino colors keyed by shape ---
COLORS = {
    'I': (0, 200, 220),
    'O': (230, 200, 0),
    'T': (170, 0, 220),
    'S': (0, 210, 80),
    'Z': (230, 40, 40),
    'J': (40, 80, 230),
    'L': (240, 140, 0),
}
# --- The seven standard tetromino shapes (base rotation matrices) ---
SHAPES = {
    'I': [[1, 1, 1, 1]],
    'O': [[1, 1],
          [1, 1]],
    'T': [[1, 1, 1],
          [0, 1, 0]],
    'S': [[0, 1, 1],
          [1, 1, 0]],
    'Z': [[1, 1, 0],
          [0, 1, 1]],
    'J': [[1, 0, 0],
          [1, 1, 1]],
    'L': [[0, 0, 1],
          [1, 1, 1]],
}
SHAPE_KEYS = list(SHAPES.keys())
# --- Drop speed configuration (milliseconds) ---
BASE_DROP_INTERVAL = 800    # gravity interval at level 1
MIN_DROP_INTERVAL = 80      # fastest allowed gravity interval
DROP_INTERVAL_STEP = 70     # interval reduction per level
# --- Scoring ---
LINE_SCORES = {1: 100, 2: 300, 3: 500, 4: 800}
LINES_PER_LEVEL = 10        # lines cleared to reach the next level
# --- Key repeat (milliseconds) ---
INITIAL_DELAY = 250         # delay before a held key starts repeating
REPEAT_DELAY = 60           # interval between repeats while held