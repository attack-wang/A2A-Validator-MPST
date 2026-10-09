'''Configuration constants for the match-3 puzzle game.'''
# Window / layout
WINDOW_WIDTH = 640
WINDOW_HEIGHT = 760
BOARD_ROWS = 8
BOARD_COLS = 8
CELL_SIZE = 64
BOARD_WIDTH = BOARD_COLS * CELL_SIZE  # 512
BOARD_HEIGHT = BOARD_ROWS * CELL_SIZE  # 512
BOARD_OFFSET_X = (WINDOW_WIDTH - BOARD_WIDTH) // 2  # 64
BOARD_OFFSET_Y = 180  # leave room for HUD on top
# HUD
HUD_HEIGHT = 160
# Colors (R, G, B)
COLOR_BACKGROUND = (30, 30, 46)
COLOR_BOARD_LIGHT = (52, 52, 78)
COLOR_BOARD_DARK = (44, 44, 66)
COLOR_BOARD_BORDER = (120, 120, 160)
COLOR_TEXT = (240, 240, 255)
COLOR_TEXT_DIM = (160, 160, 190)
COLOR_SELECTED = (255, 255, 255)
COLOR_HOVER = (255, 255, 255)
COLOR_BUTTON = (90, 90, 140)
COLOR_BUTTON_HOVER = (120, 120, 180)
COLOR_OVERLAY = (20, 20, 35)
# Candy definitions: (name, base color, highlight color, shape)
CANDY_TYPES = [
    ("red", (235, 87, 87), (255, 140, 140), "circle"),
    ("orange", (245, 166, 35), (255, 200, 100), "square"),
    ("yellow", (247, 215, 68), (255, 240, 150), "diamond"),
    ("green", (106, 204, 101), (150, 235, 145), "hexagon"),
    ("blue", (75, 145, 235), (130, 190, 255), "circle"),
    ("purple", (155, 100, 220), (200, 150, 255), "square"),
]
NUM_CANDY_TYPES = len(CANDY_TYPES)
# Gameplay
STARTING_MOVES = 30
TARGET_SCORE = 5000
BASE_POINTS_PER_CANDY = 50
MATCH_BONUS_4 = 100      # extra points for a 4-match
MATCH_BONUS_5 = 250      # extra points for a 5+ match
CHAIN_MULTIPLIER_STEP = 0.5  # chain n multiplier = 1 + (n-1)*step
# Animation timing (seconds)
SWAP_DURATION = 0.18
SWAP_BACK_DURATION = 0.18
CLEAR_DURATION = 0.25
FALL_DURATION_PER_CELL = 0.06
FALL_MIN_DURATION = 0.12
SPAWN_DROP_ROWS = 2  # extra rows new candies start above the board
# Misc
FPS = 60
SHUFFLE_ATTEMPTS = 200