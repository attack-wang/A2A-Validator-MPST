'''
settings.py
Central configuration for the Classic Snake game.
Contains all tunable constants: window dimensions, grid size, colors,
directions and the difficulty presets (speed and score multiplier).
'''
# ---------------------------------------------------------------------------
# Window / grid configuration
# ---------------------------------------------------------------------------
WINDOW_WIDTH = 640          # Playable window width in pixels
WINDOW_HEIGHT = 480         # Playable window height in pixels
GRID_SIZE = 20              # Size of one grid cell (snake segment) in pixels
# Derived grid dimensions (number of cells per axis)
GRID_WIDTH = WINDOW_WIDTH // GRID_SIZE      # 32 cells
GRID_HEIGHT = WINDOW_HEIGHT // GRID_SIZE    # 24 cells
# ---------------------------------------------------------------------------
# Frame rate limits
# ---------------------------------------------------------------------------
MENU_FPS = 30               # Refresh rate while in menus / game-over screen
# ---------------------------------------------------------------------------
# Colors (R, G, B)
# ---------------------------------------------------------------------------
COLOR_BACKGROUND = (18, 18, 18)
COLOR_GRID_LINE = (32, 32, 32)
COLOR_BORDER = (90, 90, 90)
COLOR_SNAKE_HEAD = (0, 220, 90)
COLOR_SNAKE_BODY = (0, 160, 70)
COLOR_FOOD = (230, 60, 60)
COLOR_TEXT = (235, 235, 235)
COLOR_TEXT_DIM = (150, 150, 150)
COLOR_TITLE = (0, 220, 90)
COLOR_HIGHLIGHT = (255, 210, 60)
# ---------------------------------------------------------------------------
# Directions (unit vectors on the grid)
# ---------------------------------------------------------------------------
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)
# ---------------------------------------------------------------------------
# Difficulty presets
# speed      -> snake moves per second
# multiplier -> points awarded per food item
# ---------------------------------------------------------------------------
DIFFICULTY_LEVELS = {
    "easy":   {"speed": 6,  "multiplier": 1, "label": "Easy"},
    "medium": {"speed": 10, "multiplier": 2, "label": "Medium"},
    "hard":   {"speed": 16, "multiplier": 3, "label": "Hard"},
}
DIFFICULTY_ORDER = ["easy", "medium", "hard"]