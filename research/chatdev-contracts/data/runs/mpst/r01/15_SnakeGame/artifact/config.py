'''
config.py
Contains all global configuration constants for the Snake game,
including board dimensions, colors, directions, and difficulty settings.
'''
# Board settings
CELL_SIZE = 20
GRID_WIDTH = 30   # number of cells horizontally
GRID_HEIGHT = 20  # number of cells vertically
BOARD_WIDTH = CELL_SIZE * GRID_WIDTH
BOARD_HEIGHT = CELL_SIZE * GRID_HEIGHT
HUD_HEIGHT = 40   # extra space at top for score display
WINDOW_WIDTH = BOARD_WIDTH
WINDOW_HEIGHT = BOARD_HEIGHT + HUD_HEIGHT
FPS = 60
# Colors (R, G, B)
COLOR_BACKGROUND = (15, 15, 15)
COLOR_GRID = (30, 30, 30)
COLOR_BORDER = (200, 200, 200)
COLOR_SNAKE_HEAD = (0, 200, 80)
COLOR_SNAKE_BODY = (0, 150, 60)
COLOR_SNAKE_OUTLINE = (10, 60, 30)    # FIX: dark outline around snake segments
COLOR_FOOD = (220, 40, 40)
COLOR_FOOD_OUTLINE = (120, 10, 10)    # FIX: dark outline around the food circle
COLOR_TEXT = (240, 240, 240)
COLOR_MENU_TITLE = (0, 200, 80)
COLOR_MENU_HIGHLIGHT = (255, 215, 0)
# Directions as (dx, dy) tuples
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)
# Difficulty levels: name -> move interval in milliseconds (lower = faster)
DIFFICULTY_LEVELS = {
    "Easy": 200,
    "Medium": 120,
    "Hard": 70,
}
# Points awarded per food
SCORE_PER_FOOD = 10