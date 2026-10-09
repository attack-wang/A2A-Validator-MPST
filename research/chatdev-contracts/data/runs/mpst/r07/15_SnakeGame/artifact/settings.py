'''
settings.py
Configuration constants for the Snake game.
'''
# Window dimensions (in pixels)
WINDOW_WIDTH = 640
WINDOW_HEIGHT = 480
# Grid configuration
GRID_SIZE = 20  # Size of each cell in pixels
GRID_WIDTH = WINDOW_WIDTH // GRID_SIZE   # 32 columns
GRID_HEIGHT = WINDOW_HEIGHT // GRID_SIZE # 24 rows
# Frame rate cap
MAX_FPS = 60
# Colors (R, G, B)
BLACK = (15, 15, 15)
GRID_COLOR = (30, 30, 30)
WHITE = (240, 240, 240)
GREEN = (0, 200, 80)
DARK_GREEN = (0, 150, 60)
RED = (220, 40, 40)
GRAY = (120, 120, 120)
YELLOW = (255, 215, 0)
BLUE = (60, 120, 220)
# Snake and food rendering colors (unified names used by snake.py / food.py)
HEAD_COLOR = (0, 220, 100)
BODY_COLOR = (0, 160, 70)
OUTLINE_COLOR = (10, 60, 30)
FOOD_COLOR = (230, 60, 60)
FOOD_OUTLINE = (120, 20, 20)
# Directions
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)
# Difficulty levels: name -> (snake speed in moves/sec, score multiplier)
DIFFICULTY_LEVELS = {
    "Easy":   {"speed": 6,  "multiplier": 1},
    "Medium": {"speed": 10, "multiplier": 2},
    "Hard":   {"speed": 15, "multiplier": 3},
    "Insane": {"speed": 22, "multiplier": 5},
}
# Font settings
FONT_NAME = None  # Use pygame default font