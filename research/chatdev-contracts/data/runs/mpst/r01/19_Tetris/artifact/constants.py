'''
Global configuration constants for the Tetris game, including board
dimensions, colors, tetromino shape definitions, scoring rules and
difficulty progression parameters.
'''
# ----- Board dimensions -----
BOARD_COLS = 10          # Number of columns on the playfield
BOARD_ROWS = 20          # Number of visible rows on the playfield
CELL_SIZE = 30           # Pixel size of a single board cell
# ----- Window / UI layout -----
SIDEBAR_WIDTH = 240                          # Width of the right-hand info panel
SCREEN_WIDTH = BOARD_COLS * CELL_SIZE + SIDEBAR_WIDTH
SCREEN_HEIGHT = BOARD_ROWS * CELL_SIZE
FPS = 60                                     # Target frames per second
# ----- Colors -----
COLOR_BG = (18, 18, 26)          # Window background
COLOR_BOARD = (24, 24, 34)       # Playfield background
COLOR_GRID = (42, 42, 56)        # Playfield grid lines
COLOR_BORDER = (120, 120, 150)   # Playfield border
COLOR_TEXT = (235, 235, 245)     # Regular text
COLOR_ACCENT = (255, 210, 60)    # Highlighted text (score values)
COLOR_GHOST = (150, 150, 170)    # Ghost (landing preview) piece
COLOR_OVERLAY = (10, 10, 16)     # Game-over overlay
# ----- Tetromino definitions -----
# Each shape is stored as a matrix of 0/1; rotation is done on the matrix.
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
TETROMINO_COLORS = {
    'I': (0, 190, 210),
    'O': (225, 190, 30),
    'T': (165, 70, 215),
    'S': (70, 200, 90),
    'Z': (215, 70, 70),
    'J': (70, 100, 220),
    'L': (225, 140, 40),
}
# ----- Scoring -----
LINE_SCORES = {1: 100, 2: 300, 3: 500, 4: 800}  # Base points per simultaneous line clear
SOFT_DROP_SCORE = 1    # Points per cell moved down with the soft drop
HARD_DROP_SCORE = 2    # Points per cell moved down with the hard drop
# ----- Difficulty progression -----
LINES_PER_LEVEL = 10        # Lines cleared needed to reach the next level
BASE_DROP_INTERVAL = 0.8    # Seconds between automatic drops at level 1
SPEED_FACTOR = 0.85         # Drop interval multiplier applied per level
MIN_DROP_INTERVAL = 0.05    # Fastest allowed drop interval (seconds)
# ----- Input handling -----
DAS_DELAY = 0.17            # Initial delay before a held key starts repeating
DAS_REPEAT = 0.05           # Repeat interval while a movement key is held
ROTATION_KICKS = ((0, 0), (-1, 0), (1, 0), (0, -1), (-1, -1), (1, -1), (-2, 0), (2, 0))