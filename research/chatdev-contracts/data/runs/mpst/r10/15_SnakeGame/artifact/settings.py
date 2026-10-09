'''
settings.py
Central configuration for the Classic Snake game.
Contains grid dimensions, window size, color palette, difficulty
definitions (speed and scoring multiplier), and key bindings.
Modifying values here tunes the game without touching game logic.
This version uses tkinter keysyms so the game only needs the
Python standard library (no third-party dependencies).
'''
# Grid & window
GRID_WIDTH = 24
GRID_HEIGHT = 18
CELL_SIZE = 30
UI_BAR_HEIGHT = 60
BOARD_OFFSET_X = 0
BOARD_OFFSET_Y = UI_BAR_HEIGHT
WINDOW_WIDTH = GRID_WIDTH * CELL_SIZE
WINDOW_HEIGHT = GRID_HEIGHT * CELL_SIZE + UI_BAR_HEIGHT
WINDOW_TITLE = "Classic Snake - ChatDev"
# Colors (tkinter accepts hex strings)
COLOR_BACKGROUND = "#12121a"
COLOR_GRID_LINE = "#20202c"
COLOR_BORDER = "#5a5a6e"
COLOR_BAR = "#1c1c26"
COLOR_SNAKE_HEAD = "#00dc78"
COLOR_SNAKE_BODY = "#00a05a"
COLOR_SNAKE_BODY_ALT = "#008c50"
COLOR_FOOD = "#e63c3c"
COLOR_TEXT = "#ebebeb"
COLOR_TEXT_DIM = "#9696a0"
COLOR_HIGHLIGHT = "#ffd246"
COLOR_OVERLAY = "#0a0a10"
# Gameplay
INITIAL_SNAKE_LENGTH = 3
GROWTH_PER_FOOD = 1
START_POSITION = (GRID_WIDTH // 2, GRID_HEIGHT // 2)
START_DIRECTION = (1, 0)
# Difficulty levels
DIFFICULTIES = [
    {"key": "1", "label": "Easy",   "moves_per_second": 6,  "points_per_food": 1},
    {"key": "2", "label": "Medium", "moves_per_second": 10, "points_per_food": 2},
    {"key": "3", "label": "Hard",   "moves_per_second": 15, "points_per_food": 3},
]
DEFAULT_DIFFICULTY_INDEX = 1
SPEED_UP_EVERY_N_FOODS = 5
SPEED_UP_INCREMENT = 0.5
MAX_MOVES_PER_SECOND = 20
# Key bindings (tkinter keysyms)
DIRECTION_KEYS = {
    "Up": (0, -1),
    "Down": (0, 1),
    "Left": (-1, 0),
    "Right": (1, 0),
    "w": (0, -1),
    "s": (0, 1),
    "a": (-1, 0),
    "d": (1, 0),
    "W": (0, -1),
    "S": (0, 1),
    "A": (-1, 0),
    "D": (1, 0),
}
DIFFICULTY_KEYS = {"1": 0, "2": 1, "3": 2}
CONFIRM_KEYS = ("Return", "KP_Enter", "space")
PAUSE_KEYS = ("p", "P")
BACK_KEY = "Escape"