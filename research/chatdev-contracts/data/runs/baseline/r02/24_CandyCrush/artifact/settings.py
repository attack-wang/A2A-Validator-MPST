"""Configuration constants for the Candy Match game."""
# Window
WINDOW_WIDTH = 640
WINDOW_HEIGHT = 760
FPS = 60
GRID_ROWS = 8
GRID_COLS = 8
CELL_SIZE = 64
BOARD_TOP = 150
BOARD_LEFT = (WINDOW_WIDTH - GRID_COLS * CELL_SIZE) // 2  # 64
NUM_CANDY_TYPES = 6
CANDY_COLORS = [
    (237, 60, 60),    # red
    (255, 143, 43),   # orange
    (255, 214, 64),   # yellow
    (88, 200, 90),    # green
    (64, 140, 255),   # blue
    (176, 90, 240),   # purple
]
CANDY_NAMES = ["Cherry", "Orange", "Lemon", "Apple", "Blueberry", "Grape"]
# Colors (UI)
BACKGROUND_COLOR = (30, 30, 46)
PANEL_COLOR = (49, 50, 68)
BOARD_BG_COLOR = (24, 24, 37)
CELL_COLOR_A = (38, 38, 58)
CELL_COLOR_B = (33, 33, 51)
TEXT_COLOR = (240, 240, 250)
ACCENT_COLOR = (250, 179, 135)
SELECT_COLOR = (255, 255, 255)
# Scoring
SCORE_PER_CANDY = 50
CHAIN_MULTIPLIERS = [1, 2, 3, 5, 8]
MATCH4_BONUS = 100
MATCH5_BONUS = 300
# Game rules
INITIAL_MOVES = 30
# Animation
SWAP_DURATION = 0.18
CLEAR_DURATION = 0.25
FALL_ACCELERATION = 4000
FALL_MAX_SPEED = 1400
SELECT_PULSE_SPEED = 6.0
# Fonts
FONT_NAME = None