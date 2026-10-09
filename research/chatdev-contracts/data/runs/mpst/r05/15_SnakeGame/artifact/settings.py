'''
settings.py
Global configuration constants for the Snake game, including colors,
grid dimensions, difficulty levels, HUD layout, and font settings.
'''
# Window and grid configuration
GRID_SIZE = 20          # Number of cells per row/column
CELL_SIZE = 30          # Pixel size of each cell
WINDOW_SIZE = GRID_SIZE * CELL_SIZE  # Window width/height in pixels
HUD_HEIGHT = 60         # Height (pixels) of the score/difficulty bar beneath the board
FPS = 60                # Base frame rate for rendering
# Colors (R, G, B)
COLOR_BACKGROUND = (18, 18, 18)
COLOR_GRID = (40, 40, 40)
COLOR_BORDER = (200, 200, 200)
COLOR_SNAKE_HEAD = (0, 200, 80)
COLOR_SNAKE_BODY = (0, 150, 60)
COLOR_FOOD = (220, 40, 40)
COLOR_TEXT = (240, 240, 240)
COLOR_TEXT_DIM = (150, 150, 150)
COLOR_MENU_HIGHLIGHT = (0, 200, 80)
# Difficulty levels: name -> snake move interval in milliseconds
DIFFICULTY_LEVELS = {
    "Easy": 200,
    "Medium": 120,
    "Hard": 70,
}
# Default difficulty
DEFAULT_DIFFICULTY = "Medium"
# Font settings
FONT_NAME = None        # Use pygame default font
FONT_SIZE_LARGE = 48
FONT_SIZE_MEDIUM = 32
FONT_SIZE_SMALL = 24
# Scoring
SCORE_PER_FOOD = 10