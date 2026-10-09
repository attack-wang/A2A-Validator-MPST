'''
settings.py
Global configuration constants for the Snake game: window dimensions,
grid parameters, colors, fonts, and difficulty level definitions.
'''
# ---------- Window / Grid ----------
GRID_SIZE = 20                      # Size of one grid cell in pixels
GRID_WIDTH = 30                     # Number of cells horizontally
GRID_HEIGHT = 20                    # Number of cells vertically
WINDOW_WIDTH = GRID_SIZE * GRID_WIDTH    # 600 px
WINDOW_HEIGHT = GRID_SIZE * GRID_HEIGHT  # 400 px
# Frame rate cap for the rendering loop (game speed is controlled separately)
FPS = 60
# ---------- Colors (R, G, B) ----------
COLOR_BACKGROUND = (18, 18, 18)
COLOR_GRID = (30, 30, 30)
COLOR_BORDER = (80, 80, 80)
COLOR_SNAKE_HEAD = (0, 200, 80)
COLOR_SNAKE_BODY = (0, 150, 60)
COLOR_FOOD = (220, 40, 40)
COLOR_TEXT = (240, 240, 240)
COLOR_TEXT_DIM = (150, 150, 150)
COLOR_MENU_HIGHLIGHT = (0, 200, 80)
COLOR_GAME_OVER = (220, 60, 60)
# ---------- Directions ----------
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)
# ---------- Difficulty levels ----------
# speed: grid moves per second; score_multiplier: points per food
DIFFICULTIES = {
    "Easy":   {"speed": 6,  "score_multiplier": 1},
    "Medium": {"speed": 10, "score_multiplier": 2},
    "Hard":   {"speed": 15, "score_multiplier": 3},
}
DEFAULT_DIFFICULTY = "Medium"