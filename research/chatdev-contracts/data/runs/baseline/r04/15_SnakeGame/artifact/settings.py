'''
settings.py
Central configuration for the Classic Snake game.
Defines board dimensions, cell size, movement directions, difficulty levels,
color palette, timing constants, and the high-score persistence path.
Changing values here tunes the game without touching game logic.
'''
# ------------------------- Board / grid ------------------------- #
GRID_WIDTH = 30          # playable cells horizontally
GRID_HEIGHT = 20         # playable cells vertically
CELL_SIZE = 24           # pixels per grid cell
HUD_HEIGHT = 48          # pixel height of the score bar under the board
SCREEN_WIDTH = GRID_WIDTH * CELL_SIZE          # 720
SCREEN_HEIGHT = GRID_HEIGHT * CELL_SIZE + HUD_HEIGHT  # 528
# ------------------------- Directions --------------------------- #
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)
# ------------------------- Difficulty --------------------------- #
# "fps" is the snake's moves per second for each level.
DIFFICULTY_LEVELS = {
    "1": {"label": "Easy",   "fps": 6},
    "2": {"label": "Normal", "fps": 10},
    "3": {"label": "Hard",   "fps": 15},
}
BASE_FPS = 60   # render rate of the playing loop
MENU_FPS = 30   # render rate of menu / game-over loops
# ------------------------- Colors ------------------------------- #
COLOR_BACKGROUND = (18, 18, 28)
COLOR_BOARD = (26, 26, 40)
COLOR_GRID = (36, 36, 54)
COLOR_SNAKE_HEAD = (80, 220, 120)
COLOR_SNAKE_BODY = (50, 160, 90)
COLOR_FOOD = (230, 70, 70)
COLOR_TEXT = (235, 235, 235)
COLOR_TEXT_DIM = (150, 150, 165)
COLOR_OVERLAY = (10, 10, 18)
# ------------------------- Persistence -------------------------- #
HIGH_SCORE_FILE = "high_score.txt"