"""
constants.py
Global configuration constants for the Candy Match game: window layout,
board dimensions, gameplay tuning, colors, and animation timings.
"""
# ---------------------------------------------------------------------------
# Window / layout
# ---------------------------------------------------------------------------
WINDOW_WIDTH = 640
WINDOW_HEIGHT = 720
GRID_SIZE = 8                # board is GRID_SIZE x GRID_SIZE cells
CELL_SIZE = 64               # pixel size of one cell
BOARD_PIXEL_SIZE = GRID_SIZE * CELL_SIZE
BOARD_OFFSET_X = (WINDOW_WIDTH - BOARD_PIXEL_SIZE) // 2
BOARD_OFFSET_Y = 150         # top HUD occupies the space above the board
FPS = 60
# ---------------------------------------------------------------------------
# Gameplay tuning
# ---------------------------------------------------------------------------
NUM_CANDY_TYPES = 6
INITIAL_MOVES = 30
TARGET_SCORE = 5000          # reaching this score before moves run out = victory
SCORE_PER_CANDY = 60         # base points per cleared candy
COMBO_BONUS_STEP = 0.5       # chain n scores with multiplier 1 + (n-1)*step
# ---------------------------------------------------------------------------
# Animation timings (seconds)
# ---------------------------------------------------------------------------
SWAP_DURATION = 0.16
SWAP_BACK_DURATION = 0.16
CLEAR_DURATION = 0.28
FALL_SECONDS_PER_CELL = 0.055
FALL_MIN_DURATION = 0.15
FLOAT_TEXT_DURATION = 0.9
# ---------------------------------------------------------------------------
# Colors
# ---------------------------------------------------------------------------
COLOR_BACKGROUND = (24, 26, 38)
COLOR_BOARD_A = (52, 56, 78)      # checkerboard tile (dark)
COLOR_BOARD_B = (60, 65, 90)      # checkerboard tile (light)
COLOR_BOARD_BORDER = (120, 130, 170)
COLOR_SELECTION = (255, 230, 120)
COLOR_TEXT = (240, 240, 250)
COLOR_TEXT_DIM = (150, 155, 180)
COLOR_ACCENT = (255, 170, 60)
COLOR_PANEL = (34, 37, 54)
COLOR_BUTTON = (70, 130, 220)
COLOR_BUTTON_HOVER = (95, 155, 240)
COLOR_GAME_OVER_BG = (15, 15, 25)
# Candy palette: one base color per candy type
CANDY_COLORS = [
    (235, 87, 87),    # red
    (245, 148, 50),   # orange
    (250, 210, 70),   # yellow
    (106, 200, 95),   # green
    (80, 150, 245),   # blue
    (175, 110, 235),  # purple
]