'''
Constants and configuration for the Tetris game.
'''
# Window / board dimensions
CELL_SIZE = 30
BOARD_WIDTH = 10
BOARD_HEIGHT = 20
SIDEBAR_WIDTH = 250
WINDOW_WIDTH = BOARD_WIDTH * CELL_SIZE + SIDEBAR_WIDTH
WINDOW_HEIGHT = BOARD_HEIGHT * CELL_SIZE
# Colors (R, G, B)
BLACK = (15, 15, 25)
GRID_COLOR = (40, 40, 55)
BORDER_COLOR = (120, 120, 140)
WHITE = (240, 240, 240)
GRAY = (130, 130, 130)
# Tetromino colors
COLORS = {
    'I': (0, 200, 220),
    'O': (230, 200, 0),
    'T': (170, 0, 220),
    'S': (0, 210, 70),
    'Z': (230, 40, 40),
    'J': (40, 80, 230),
    'L': (240, 140, 0),
}
# Game speed
BASE_DROP_INTERVAL = 800  # ms per automatic drop at level 1
MIN_DROP_INTERVAL = 80
SPEEDUP_PER_LEVEL = 70  # ms faster per level
# Scoring
LINE_SCORES = {1: 100, 2: 300, 3: 500, 4: 800}
SOFT_DROP_SCORE = 1
HARD_DROP_SCORE = 2
LINES_PER_LEVEL = 10
# Input repeat for held movement keys
MOVE_REPEAT_DELAY = 170  # ms before auto-repeat kicks in
MOVE_REPEAT_INTERVAL = 45  # ms between repeated moves
# FPS
FPS = 60