'''Central configuration constants for the match-3 puzzle game.'''
# --- Window ---
WINDOW_WIDTH = 640
WINDOW_HEIGHT = 780
FPS = 60
TITLE = "Candy Match"
# --- Board geometry ---
ROWS = 8
COLS = 8
CELL_SIZE = 64
BOARD_WIDTH = COLS * CELL_SIZE
BOARD_HEIGHT = ROWS * CELL_SIZE
BOARD_X = (WINDOW_WIDTH - BOARD_WIDTH) // 2
BOARD_Y = 170
# --- Candies ---
NUM_CANDY_TYPES = 6
CANDY_COLORS = {
    0: (237, 66, 69),    # red
    1: (255, 149, 0),    # orange
    2: (255, 214, 0),    # yellow
    3: (76, 217, 100),   # green
    4: (0, 122, 255),    # blue
    5: (175, 82, 222),   # purple
}
# --- Game rules ---
INITIAL_MOVES = 30
TARGET_SCORE = 2500
BASE_POINTS = 60          # points per cleared candy
LENGTH_BONUS = 40         # extra points per candy beyond 3 in a run
CHAIN_STEP = 0.5          # cascade multiplier increment per chain level
SHUFFLE_LIMIT = 60        # safety cap for shuffle attempts
# --- Timing / animation (seconds) ---
SWAP_DURATION = 0.18
CLEAR_DURATION = 0.25
FALL_INITIAL_SPEED = 150.0     # px per second
FALL_GRAVITY = 4200.0          # px per second^2
FALL_MAX_SPEED = 1400.0
SCORE_POP_DURATION = 0.6
FLOAT_TEXT_DURATION = 0.9
TOAST_DURATION = 1.6
# --- Colors (UI) ---
BACKGROUND_COLOR = (24, 26, 38)
BOARD_COLOR = (38, 41, 58)
CELL_COLOR_A = (46, 50, 70)
CELL_COLOR_B = (52, 56, 78)
BORDER_COLOR = (90, 96, 128)
TEXT_COLOR = (235, 235, 245)
MUTED_TEXT_COLOR = (150, 155, 180)
ACCENT_COLOR = (255, 209, 102)
DANGER_COLOR = (255, 105, 97)
OVERLAY_COLOR = (12, 13, 20)
SELECT_COLOR = (255, 255, 255)