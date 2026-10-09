'''
settings.py
Central configuration for the Tetris game: board dimensions, the seven
standard tetromino shapes (I, O, T, S, Z, J, L), their guideline colors,
scoring values, level progression and gravity timing constants.
'''
# Board dimensions (in cells)
COLS = 10
ROWS = 20
CELL_SIZE = 30
# Sidebar / window layout
SIDEBAR_WIDTH = 220
WINDOW_WIDTH = COLS * CELL_SIZE + SIDEBAR_WIDTH
WINDOW_HEIGHT = ROWS * CELL_SIZE
# The seven standard tetromino shapes (I, O, T, S, Z, J, L)
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
# Standard guideline colors (R, G, B)
SHAPE_COLORS = {
    'I': (0, 240, 240),    # cyan
    'O': (240, 240, 0),    # yellow
    'T': (160, 0, 240),    # purple
    'S': (0, 240, 0),      # green
    'Z': (240, 0, 0),      # red
    'J': (0, 0, 240),      # blue
    'L': (240, 160, 0),    # orange
}
# Scoring
LINE_SCORES = {1: 100, 2: 300, 3: 500, 4: 800}
SOFT_DROP_SCORE = 1
HARD_DROP_SCORE = 2
# Level progression / gravity (drop interval shrinks as level rises)
LINES_PER_LEVEL = 10
BASE_DROP_INTERVAL = 800      # ms per row at level 1
MIN_DROP_INTERVAL = 100       # fastest gravity
DROP_SPEEDUP_PER_LEVEL = 70   # ms faster per level
# UI colors (R, G, B)
COLOR_BG = (18, 18, 26)
COLOR_GRID = (40, 40, 55)
COLOR_GRID_BORDER = (90, 90, 120)
COLOR_TEXT = (230, 230, 235)
COLOR_PANEL = (28, 28, 40)
COLOR_PANEL_BORDER = (90, 90, 120)
COLOR_GAME_OVER = (255, 80, 80)
COLOR_PAUSED = (255, 220, 120)