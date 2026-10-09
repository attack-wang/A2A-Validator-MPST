'''
config.py
Global configuration constants for the Snake game: window dimensions,
grid geometry, colors, fonts and difficulty presets.
'''
# --- Grid & window geometry -------------------------------------------------
CELL_SIZE = 30          # Pixel size of one grid cell
GRID_WIDTH = 20         # Number of cells horizontally
GRID_HEIGHT = 20        # Number of cells vertically
HUD_HEIGHT = 60         # Height of the top panel that shows the score
BOARD_WIDTH = GRID_WIDTH * CELL_SIZE    # 600 px
BOARD_HEIGHT = GRID_HEIGHT * CELL_SIZE  # 600 px
WINDOW_WIDTH = BOARD_WIDTH              # 600 px
WINDOW_HEIGHT = BOARD_HEIGHT + HUD_HEIGHT  # 660 px
WINDOW_TITLE = "Classic Snake - ChatDev"
# --- Frame rate -------------------------------------------------------------
FPS = 60  # Rendering frame rate; game logic ticks are derived from difficulty
# --- Colors (R, G, B) -------------------------------------------------------
COLOR_BACKGROUND   = (18, 18, 24)
COLOR_BOARD_A      = (26, 26, 34)
COLOR_BOARD_B      = (32, 32, 42)
COLOR_BORDER       = (70, 70, 90)
COLOR_SNAKE_HEAD   = (0, 200, 120)
COLOR_SNAKE_BODY   = (0, 150, 95)
COLOR_SNAKE_EDGE   = (0, 90, 60)
COLOR_FOOD         = (230, 60, 60)
COLOR_TEXT         = (235, 235, 235)
COLOR_TEXT_DIM     = (150, 150, 160)
COLOR_HUD_BG       = (10, 10, 14)
COLOR_OVERLAY      = (0, 0, 0, 180)  # RGBA for translucent overlays
COLOR_ACCENT       = (255, 200, 60)
# --- Directions -------------------------------------------------------------
UP    = (0, -1)
DOWN  = (0, 1)
LEFT  = (-1, 0)
RIGHT = (1, 0)
# --- Difficulty presets -----------------------------------------------------
DIFFICULTIES = {
    1: {"name": "Easy",   "speed": 5,  "points_per_food": 10},
    2: {"name": "Medium", "speed": 9,  "points_per_food": 15},
    3: {"name": "Hard",   "speed": 14, "points_per_food": 20},
    4: {"name": "Insane", "speed": 20, "points_per_food": 30},
}
DEFAULT_DIFFICULTY = 2  # Medium
# --- Fonts ------------------------------------------------------------------
FONT_NAME = None  # None -> pygame default font
# --- Persistence ------------------------------------------------------------
HIGH_SCORE_FILE = "snake_high_score.json"  # High score is kept between sessions