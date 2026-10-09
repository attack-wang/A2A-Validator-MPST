'''
settings.py
Global configuration constants for the Snake game.
'''
# ------------------------------------------------------------------ #
# Grid / window geometry
# ------------------------------------------------------------------ #
GRID_SIZE = 32                  # pixels per cell
GRID_WIDTH = 24                 # cells horizontally
GRID_HEIGHT = 18                # cells vertically
HUD_HEIGHT = 56                 # pixels reserved for the score bar
WINDOW_WIDTH = GRID_WIDTH * GRID_SIZE            # 768
WINDOW_HEIGHT = HUD_HEIGHT + GRID_HEIGHT * GRID_SIZE  # 632
FPS = 60                        # render frame rate (logic uses per-difficulty speed)
# ------------------------------------------------------------------ #
# Fonts
# ------------------------------------------------------------------ #
FONT_SIZE_HUD = 24
FONT_SIZE_TITLE = 48
FONT_SIZE_MENU = 30
FONT_SIZE_MESSAGE = 22
FONT_SIZE_SMALL = 16
# ------------------------------------------------------------------ #
# Directions (dx, dy)
# ------------------------------------------------------------------ #
DIR_UP = (0, -1)
DIR_DOWN = (0, 1)
DIR_LEFT = (-1, 0)
DIR_RIGHT = (1, 0)
# ------------------------------------------------------------------ #
# Colors (R, G, B)
# ------------------------------------------------------------------ #
COLOR_BACKGROUND = (18, 18, 24)
COLOR_GRID_A = (28, 30, 38)
COLOR_GRID_B = (24, 26, 33)
COLOR_HUD = (34, 36, 46)
COLOR_HUD_TEXT = (230, 230, 235)
COLOR_TEXT = (240, 240, 245)
COLOR_TITLE = (80, 220, 120)
COLOR_SNAKE_HEAD = (70, 200, 110)
COLOR_SNAKE_BODY = (45, 160, 85)
COLOR_SNAKE_BORDER = (20, 60, 35)
COLOR_FOOD = (220, 70, 70)
COLOR_FOOD_HIGHLIGHT = (255, 160, 160)
COLOR_MENU_HIGHLIGHT = (255, 210, 70)
COLOR_MENU_NORMAL = (170, 175, 190)
# ------------------------------------------------------------------ #
# Difficulty levels: moves per second + HUD accent color
# ------------------------------------------------------------------ #
DIFFICULTIES = {
    "Easy":   {"speed": 6,  "color": (120, 200, 255)},
    "Medium": {"speed": 10, "color": (255, 210, 70)},
    "Hard":   {"speed": 15, "color": (255, 110, 110)},
}
DIFFICULTY_ORDER = ["Easy", "Medium", "Hard"]