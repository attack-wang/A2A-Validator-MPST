'''
Global configuration constants for the Candy Match game.
'''
# --- Window ---
WINDOW_WIDTH = 640
WINDOW_HEIGHT = 780
FPS = 60
TITLE = "Candy Match Deluxe"
# --- Board ---
GRID_SIZE = 8
CELL_SIZE = 64
BOARD_PIXEL_SIZE = GRID_SIZE * CELL_SIZE
BOARD_OFFSET_X = (WINDOW_WIDTH - BOARD_PIXEL_SIZE) // 2
BOARD_OFFSET_Y = 200
# --- Colors ---
WHITE = (255, 255, 255)
BLACK = (15, 15, 25)
DARK_BG = (34, 32, 52)
BOARD_LIGHT = (58, 54, 80)
BOARD_DARK = (46, 43, 66)
GRID_LINE = (28, 26, 44)
HUD_TEXT = (255, 255, 255)
ACCENT = (255, 200, 60)
SELECT_COLOR = (255, 255, 255)
OVERLAY_COLOR = (10, 10, 20)
BUTTON_COLOR = (72, 152, 230)
BUTTON_HOVER_COLOR = (106, 204, 101)
# --- Candies ---
NUM_CANDY_TYPES = 6
CANDY_COLORS = [
    (237, 76, 103),
    (245, 130, 48),
    (255, 210, 63),
    (106, 204, 101),
    (72, 152, 230),
    (155, 89, 220),
]
CANDY_DARK_COLORS = [
    (max(0, r - 70), max(0, g - 70), max(0, b - 70))
    for (r, g, b) in CANDY_COLORS
]
# --- Animation ---
SWAP_DURATION = 0.22
CLEAR_DURATION = 0.28
FALL_ACCELERATION = 4000
MAX_FALL_SPEED = 1400
SHUFFLE_MESSAGE_TIME = 1.2
# --- Scoring ---
BASE_POINTS_PER_CANDY = 60
MATCH_LENGTH_BONUS = {4: 100, 5: 250, 6: 400, 7: 600, 8: 800}
CHAIN_MULTIPLIER_STEP = 1.0
# --- Game rules ---
STARTING_MOVES = 25
TARGET_SCORE = 6000