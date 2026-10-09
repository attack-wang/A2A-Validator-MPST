'''
settings.py
Global configuration constants for the Snake game, including window
dimensions, grid layout, colors, fonts, difficulty presets, and file paths.
'''
import os
# ---------------------------------------------------------------------------
# Window / grid configuration
# ---------------------------------------------------------------------------
GRID_SIZE = 20                      # Pixel size of a single grid cell
GRID_WIDTH = 30                     # Number of cells horizontally
GRID_HEIGHT = 20                    # Number of cells vertically
WINDOW_WIDTH = GRID_SIZE * GRID_WIDTH    # 600 px
WINDOW_HEIGHT = GRID_SIZE * GRID_HEIGHT  # 400 px
# Extra vertical space reserved for the score / status bar
HUD_HEIGHT = 40
WINDOW_HEIGHT += HUD_HEIGHT
# Rendering frame rate (frames per second of the main loop)
RENDER_FPS = 60
# ---------------------------------------------------------------------------
# Colors (R, G, B)
# ---------------------------------------------------------------------------
COLOR_BACKGROUND = (18, 18, 18)
COLOR_GRID_LINE = (32, 32, 32)
COLOR_BORDER = (70, 70, 70)
COLOR_SNAKE_HEAD = (0, 200, 80)
COLOR_SNAKE_BODY = (0, 160, 60)
COLOR_SNAKE_BODY_ALT = (0, 140, 55)
COLOR_FOOD = (220, 40, 40)
COLOR_TEXT = (240, 240, 240)
COLOR_TEXT_DIM = (150, 150, 150)
COLOR_HUD_BG = (10, 10, 10)
COLOR_MENU_HIGHLIGHT = (255, 200, 0)
COLOR_OVERLAY = (0, 0, 0, 180)
# ---------------------------------------------------------------------------
# Gameplay configuration
# ---------------------------------------------------------------------------
INITIAL_SNAKE_LENGTH = 3
SCORE_PER_FOOD = 10
# Difficulty presets: moves per second and score multiplier
DIFFICULTIES = {
    "Easy":   {"speed": 5,  "multiplier": 1},
    "Medium": {"speed": 10, "multiplier": 2},
    "Hard":   {"speed": 15, "multiplier": 3},
    "Insane": {"speed": 22, "multiplier": 4},
}
DEFAULT_DIFFICULTY = "Medium"
# Direction vectors (dx, dy)
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)
# ---------------------------------------------------------------------------
# Persistence
# ---------------------------------------------------------------------------
HIGHSCORE_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "highscore.json")
# ---------------------------------------------------------------------------
# Fonts
# ---------------------------------------------------------------------------
FONT_NAME = "consolas"   # fallback handled in ui.py
FONT_SMALL = 16
FONT_MEDIUM = 22
FONT_LARGE = 32
FONT_TITLE = 48