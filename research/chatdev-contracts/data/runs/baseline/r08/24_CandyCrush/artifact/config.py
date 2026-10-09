'''Configuration module: central constants for window, board, gameplay, animation, and colors.'''
# Window
WINDOW_WIDTH = 640
WINDOW_HEIGHT = 720
FPS = 60
TITLE = "Candy Crush Saga-style Match-3"
# Board
GRID_ROWS = 8
GRID_COLS = 8
CELL_SIZE = 64
BOARD_WIDTH = GRID_COLS * CELL_SIZE
BOARD_HEIGHT = GRID_ROWS * CELL_SIZE
BOARD_X = (WINDOW_WIDTH - BOARD_WIDTH) // 2
BOARD_Y = 160
# Gameplay
NUM_CANDY_TYPES = 6
MOVES_LIMIT = 30
TIME_LIMIT_SECONDS = 180
BASE_POINTS = 60
RUN_BONUS_PER_EXTRA = 150
CHAIN_MULTIPLIER = 1  # chain multiplier applied as chain count
# Animation
SWAP_SPEED = 480
FALL_SPEED = 900
FALL_ACCELERATION = 2400
CLEAR_DURATION = 0.25
# Hint
HINT_DELAY_SECONDS = 5.0
# Colors
BACKGROUND_COLOR = (24, 28, 46)
BOARD_COLOR_A = (52, 60, 88)
BOARD_COLOR_B = (44, 52, 78)
BOARD_BORDER_COLOR = (90, 100, 140)
TEXT_COLOR = (235, 235, 245)
TEXT_DIM_COLOR = (150, 158, 180)
ACCENT_COLOR = (255, 200, 90)
OVERLAY_COLOR = (10, 12, 24)
SELECTED_COLOR = (255, 255, 255)
HINT_COLOR = (120, 220, 255)
# Candy types: color, dark (outline/shade), shape
CANDY_TYPES = [
    {"color": (230, 70, 70), "dark": (150, 30, 30), "shape": "circle"},      # red
    {"color": (250, 160, 40), "dark": (170, 90, 10), "shape": "square"},     # orange
    {"color": (250, 220, 70), "dark": (170, 140, 20), "shape": "diamond"},   # yellow
    {"color": (90, 200, 90), "dark": (40, 120, 40), "shape": "hexagon"},     # green
    {"color": (90, 140, 250), "dark": (40, 70, 160), "shape": "triangle"},   # blue
    {"color": (200, 110, 230), "dark": (130, 60, 160), "shape": "oval"},     # purple
]