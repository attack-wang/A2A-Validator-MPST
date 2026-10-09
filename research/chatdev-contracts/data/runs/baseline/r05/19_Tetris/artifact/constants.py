'''
constants.py
Global configuration and data tables for the Tetris game:
board dimensions, colors, the seven standard tetromino shapes,
scoring table, gravity/level progression and input timing constants.
'''
import pygame
# --- Board geometry -------------------------------------------------------
BOARD_WIDTH = 10          # playable columns
BOARD_HEIGHT = 20         # playable rows
CELL_SIZE = 30            # pixel size of one cell
PANEL_BORDER = 4          # border thickness around the board panel
# --- Window ---------------------------------------------------------------
SIDEBAR_WIDTH = 220
WINDOW_WIDTH = BOARD_WIDTH * CELL_SIZE + SIDEBAR_WIDTH + 40
WINDOW_HEIGHT = BOARD_HEIGHT * CELL_SIZE + 40
FPS = 60
# --- Colors ---------------------------------------------------------------
BLACK = (17, 17, 20)
GRID_LINE = (45, 45, 52)
BOARD_BG = (24, 24, 30)
SIDEBAR_BG = (17, 17, 20)
PANEL_BG = (28, 28, 36)
WHITE = (235, 235, 240)
GREY = (140, 140, 150)
GHOST_ALPHA = 70
COLORS = {
    'I': (0, 200, 220),      # cyan
    'O': (230, 200, 0),      # yellow
    'T': (170, 60, 200),     # purple
    'S': (60, 200, 80),      # green
    'Z': (220, 60, 60),      # red
    'J': (50, 90, 220),      # blue
    'L': (230, 140, 30),     # orange
}
# --- Shapes: the seven standard tetrominoes --------------------------------
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
# --- Scoring & progression -------------------------------------------------
LINE_SCORES = {1: 100, 2: 300, 3: 500, 4: 800}
SOFT_DROP_SCORE = 1       # points per cell moved down manually
HARD_DROP_SCORE = 2       # points per cell dropped instantly
LINES_PER_LEVEL = 10
BASE_GRAVITY_MS = 800     # gravity interval at level 1
GRAVITY_STEP_MS = 60      # interval reduction per level
MIN_GRAVITY_MS = 80       # fastest allowed interval
LOCK_DELAY_MS = 500       # time a grounded piece may still be moved
MAX_LOCK_RESETS = 15      # cap on lock-delay resets per piece
# --- Input timing (DAS = delayed auto shift) -------------------------------
DAS_DELAY = 170   # ms before auto-repeat kicks in
DAS_REPEAT = 45   # ms between repeats