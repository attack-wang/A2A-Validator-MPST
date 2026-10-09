"""Constants and configuration for the Candy Match game."""
# Window / board layout
WINDOW_WIDTH = 640
WINDOW_HEIGHT = 760
GRID_ROWS = 8
GRID_COLS = 8
CELL_SIZE = 64
BOARD_WIDTH = GRID_COLS * CELL_SIZE
BOARD_HEIGHT = GRID_ROWS * CELL_SIZE
BOARD_X = (WINDOW_WIDTH - BOARD_WIDTH) // 2
BOARD_Y = 170
# Gameplay
FPS = 60
NUM_CANDY_TYPES = 6
INITIAL_MOVES = 30
TIME_LIMIT_SECONDS = 180
TARGET_SCORE = 6000
# Scoring
SCORE_PER_CANDY = 50
LONG_MATCH_BONUS = 25  # per extra candy beyond 3 in a single run
# Animation
SWAP_DURATION = 0.18
CLEAR_DURATION = 0.25
GRAVITY_ACCELERATION = 4800.0
MAX_FALL_SPEED = 1500.0
POPUP_LIFETIME = 1.0
HINT_DURATION = 2.0
MESSAGE_DURATION = 2.0
# Colors (R, G, B)
COLOR_BACKGROUND = (30, 30, 46)
COLOR_PANEL = (44, 44, 68)
COLOR_PANEL_BORDER = (90, 90, 130)
COLOR_CELL_A = (54, 54, 82)
COLOR_CELL_B = (48, 48, 74)
COLOR_TEXT = (235, 235, 245)
COLOR_TEXT_DIM = (160, 160, 190)
COLOR_ACCENT = (255, 210, 80)
COLOR_SELECTED = (255, 255, 255)
COLOR_HINT = (120, 255, 160)
COLOR_OVERLAY = (15, 15, 25)
# Candy colors per type
CANDY_COLORS = [
    (255, 80, 95),    # red
    (255, 150, 60),   # orange
    (255, 220, 70),   # yellow
    (110, 225, 110),  # green
    (90, 160, 255),   # blue
    (200, 110, 255),  # purple
]
CANDY_HIGHLIGHTS = [ lighter versions ]  # compute in renderer instead