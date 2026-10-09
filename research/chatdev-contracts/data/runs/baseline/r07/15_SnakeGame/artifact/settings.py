'''
settings.py
Global configuration constants for the Snake game: board dimensions,
colors, directions, difficulty presets and file paths.
'''
# Board / window geometry
WINDOW_WIDTH = 640
HUD_HEIGHT = 40
WINDOW_HEIGHT = 480  # includes HUD bar
BOARD_HEIGHT = WINDOW_HEIGHT - HUD_HEIGHT  # 440
GRID_SIZE = 20
GRID_WIDTH = WINDOW_WIDTH // GRID_SIZE    # 32
GRID_HEIGHT = BOARD_HEIGHT // GRID_SIZE   # 22
# Colors
BLACK = (18, 18, 18)
GRID_LINE = (32, 32, 32)
DARK_GRAY = (45, 45, 45)
GRAY = (120, 120, 120)
WHITE = (240, 240, 240)
GREEN = (0, 200, 80)
DARK_GREEN = (0, 140, 60)
RED = (230, 60, 60)
ORANGE = (255, 160, 40)
YELLOW = (255, 215, 0)
BLUE = (70, 130, 230)
PURPLE = (170, 80, 220)
# Directions
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)
# Difficulty presets
DIFFICULTY_LEVELS = {
    "Easy":   {"fps": 6,  "multiplier": 1, "color": GREEN},
    "Medium": {"fps": 10, "multiplier": 2, "color": YELLOW},
    "Hard":   {"fps": 15, "multiplier": 3, "color": ORANGE},
    "Insane": {"fps": 22, "multiplier": 5, "color": RED},
}
DIFFICULTY_ORDER = ["Easy", "Medium", "Hard", "Insane"]
# Scoring & files
POINTS_PER_FOOD = 10
HIGH_SCORE_FILE = "highscores.json"
FONT_CANDIDATES = ["consolas", "couriernew", "dejavusansmono", "arial"]