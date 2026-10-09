'''
constants.py
Configuration constants for the Tetris game: board dimensions, colors,
scoring rules, speed progression parameters, and control timing settings.
'''
# --- Board dimensions (standard Tetris is 10 x 20) ---
BOARD_WIDTH = 10
BOARD_HEIGHT = 20
# --- Rendering geometry ---
CELL_SIZE = 30
SIDEBAR_WIDTH = 220
SCREEN_WIDTH = BOARD_WIDTH * CELL_SIZE + SIDEBAR_WIDTH
SCREEN_HEIGHT = BOARD_HEIGHT * CELL_SIZE
# --- Colors (R, G, B) ---
COLOR_BACKGROUND = (18, 18, 28)
COLOR_GRID = (45, 45, 60)
COLOR_BORDER = (200, 200, 215)
COLOR_TEXT = (235, 235, 235)
COLOR_TEXT_DIM = (150, 150, 165)
COLOR_GHOST = (120, 120, 140)
COLOR_OVERLAY = (0, 0, 0, 180)
COLORS = {
    'I': (0, 199, 230),
    'O': (241, 196, 15),
    'T': (155, 89, 220),
    'S': (46, 204, 113),
    'Z': (231, 76, 60),
    'J': (52, 101, 235),
    'L': (243, 156, 18),
}
# --- Scoring ---
LINE_SCORES = {1: 100, 2: 300, 3: 500, 4: 800}
SOFT_DROP_POINTS = 1
HARD_DROP_POINTS = 2
LINES_PER_LEVEL = 10
# --- Speed progression ---
BASE_DROP_INTERVAL = 0.8
MIN_DROP_INTERVAL = 0.05
SPEED_FACTOR = 0.85
# --- Input timing ---
DAS_DELAY = 0.17
ARR_INTERVAL = 0.045
SOFT_DROP_INTERVAL = 0.05
# --- Loop timing ---
FPS = 60