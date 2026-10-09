'''
constants.py
Global configuration constants for the Tetris game: board dimensions,
window layout, colors, tetromino shape matrices, scoring rules, and
speed/level progression parameters.
'''
# ---------------------------------------------------------------------------
# Board and window geometry
# ---------------------------------------------------------------------------
BOARD_WIDTH = 10          # number of cells horizontally
BOARD_HEIGHT = 20         # number of cells vertically
CELL_SIZE = 30            # pixel size of one cell
SIDEBAR_WIDTH = 240       # width of the info panel on the right
WINDOW_WIDTH = BOARD_WIDTH * CELL_SIZE + SIDEBAR_WIDTH
WINDOW_HEIGHT = BOARD_HEIGHT * CELL_SIZE
# ---------------------------------------------------------------------------
# Colors (R, G, B)
# ---------------------------------------------------------------------------
BLACK = (15, 15, 20)
WHITE = (240, 240, 240)
GRAY = (120, 120, 120)
DARK_GRAY = (45, 45, 55)
GRID_COLOR = (55, 55, 70)
BORDER_COLOR = (180, 180, 200)
TEXT_COLOR = (230, 230, 230)
ACCENT_COLOR = (0, 200, 255)
OVERLAY_COLOR = (0, 0, 0, 180)  # used with alpha surfaces
# Standard Tetris colors for the seven tetrominoes
COLORS = {
    'I': (0, 240, 240),    # cyan
    'O': (240, 220, 0),    # yellow
    'T': (170, 0, 240),    # purple
    'S': (0, 235, 0),      # green
    'Z': (240, 50, 50),    # red
    'J': (60, 90, 240),    # blue
    'L': (240, 150, 30),   # orange
}
# ---------------------------------------------------------------------------
# Tetromino shape matrices (1 = filled cell)
# ---------------------------------------------------------------------------
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
# ---------------------------------------------------------------------------
# Scoring rules
# ---------------------------------------------------------------------------
LINE_SCORES = {1: 100, 2: 300, 3: 500, 4: 800}  # base points per simultaneous clears
SOFT_DROP_SCORE = 1      # points per row moved with soft drop
HARD_DROP_SCORE = 2      # points per row moved with hard drop
# ---------------------------------------------------------------------------
# Level / speed progression
# ---------------------------------------------------------------------------
LINES_PER_LEVEL = 10          # lines cleared to advance one level
BASE_DROP_INTERVAL = 800.0    # ms between automatic drops at level 1
DROP_SPEEDUP_FACTOR = 0.82    # drop interval multiplier applied per level
MIN_DROP_INTERVAL = 70.0      # fastest allowed automatic drop interval (ms)