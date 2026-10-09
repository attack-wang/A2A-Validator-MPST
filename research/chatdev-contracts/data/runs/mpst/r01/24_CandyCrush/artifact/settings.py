"""Global configuration constants for the Candy Crush-style match-3 game."""
import pygame  # not needed here actually
WINDOW_WIDTH = 720
WINDOW_HEIGHT = 800
FPS = 60
TITLE = "Candy Crush Deluxe"
ROWS = 8
COLS = 8
CELL_SIZE = 64
BOARD_PIXEL_WIDTH = COLS * CELL_SIZE
BOARD_PIXEL_HEIGHT = ROWS * CELL_SIZE
BOARD_TOP = 180
BOARD_LEFT = (WINDOW_WIDTH - BOARD_PIXEL_WIDTH) // 2
# Colors
COLOR_BG = (24, 26, 38)
COLOR_BOARD_A = (38, 41, 58)
COLOR_BOARD_B = (44, 48, 68)
COLOR_BOARD_BORDER = (90, 96, 130)
COLOR_TEXT = (235, 235, 245)
COLOR_TEXT_DIM = (150, 155, 180)
COLOR_HIGHLIGHT = (255, 255, 255)
COLOR_OVERLAY = (15, 16, 24)
COLOR_BUTTON = (70, 76, 110)
COLOR_BUTTON_HOVER = (96, 104, 148)
NUM_CANDY_TYPES = 6
CANDY_TYPES = [
    {"color": (230, 70, 70),   "shape": "circle"},    # red
    {"color": (250, 160, 40),  "shape": "square"},    # orange
    {"color": (250, 210, 60),  "shape": "star"},      # yellow
    {"color": (90, 200, 90),   "shape": "diamond"},   # green
    {"color": (80, 130, 240),  "shape": "hexagon"},   # blue
    {"color": (190, 100, 230), "shape": "heart"},     # purple
]
STARTING_MOVES = 25
TIMED_MODE_SECONDS = 120
BASE_POINTS_PER_CANDY = 20
GROUP_BONUS_PER_EXTRA = 30
TARGET_SCORE_BASE = 2000
TARGET_SCORE_STEP = 1500
SHUFFLE_SEARCH_LIMIT = 20000
SWAP_DURATION = 0.18
CLEAR_DURATION = 0.25
FALL_SPEED = 1400.0
FALL_ACCELERATION = 5200.0