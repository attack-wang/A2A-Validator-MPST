'''
settings.py
Central configuration module for the Snake game.
Contains all tunable constants: window dimensions, grid geometry,
colors, fonts, keyboard bindings and the difficulty presets used
by the rest of the application.
'''
# ---------------------------------------------------------------------------
# Window / board geometry
# ---------------------------------------------------------------------------
CELL_SIZE = 20          # Pixel size of one grid cell
BOARD_WIDTH = 30        # Number of cells horizontally
BOARD_HEIGHT = 20       # Number of cells vertically
HUD_HEIGHT = 40         # Pixel height of the score bar above the board
WINDOW_WIDTH = BOARD_WIDTH * CELL_SIZE            # 600 px
WINDOW_HEIGHT = BOARD_HEIGHT * CELL_SIZE + HUD_HEIGHT  # 440 px
# ---------------------------------------------------------------------------
# Game timing
# ---------------------------------------------------------------------------
FPS = 60                    # Rendering frame rate
INITIAL_SNAKE_LENGTH = 3    # Starting body length
# Speed (moves per second) for each difficulty level
DIFFICULTIES = {
    "1": {"name": "Easy",   "speed": 6,  "color": ( 76, 175,  80)},
    "2": {"name": "Medium", "speed": 10, "color": (255, 152,   0)},
    "3": {"name": "Hard",   "speed": 16, "color": (229,  57,  53)},
}
# How much the speed increases (in moves/second) for every food eaten
SPEED_INCREMENT = 0.35
MAX_SPEED = 25
# Points awarded per food item
SCORE_PER_FOOD = 10
# ---------------------------------------------------------------------------
# Directions (grid deltas)
# ---------------------------------------------------------------------------
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)
# ---------------------------------------------------------------------------
# Colors (R, G, B)
# ---------------------------------------------------------------------------
COLOR_BACKGROUND = (18, 18, 24)
COLOR_BOARD = (26, 26, 34)
COLOR_GRID = (36, 36, 46)
COLOR_SNAKE_HEAD = (0, 200, 83)
COLOR_SNAKE_BODY = (0, 150, 63)
COLOR_FOOD = (255, 68, 68)
COLOR_TEXT = (230, 230, 230)
COLOR_TEXT_DIM = (150, 150, 150)
COLOR_HUD = (12, 12, 16)
COLOR_HIGHLIGHT = (255, 215, 64)
# ---------------------------------------------------------------------------
# Fonts
# ---------------------------------------------------------------------------
FONT_NAME = "consolas"   # falls back to pygame default when unavailable
FONT_SIZE_HUD = 20
FONT_SIZE_MENU = 28
FONT_SIZE_TITLE = 44
FONT_SIZE_SMALL = 16
# ---------------------------------------------------------------------------
# Persistence
# ---------------------------------------------------------------------------
HIGHSCORE_FILE = "highscore.json"