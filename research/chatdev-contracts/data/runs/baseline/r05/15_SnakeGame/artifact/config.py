'''
config.py
Global configuration constants for the Snake game, including window
dimensions, grid settings, colors, fonts, and difficulty level presets.
This version uses only the Python standard library (tkinter), so no
third-party packages such as pygame are required.
'''
# ---------------------------------------------------------------------------
# Window / grid settings
# ---------------------------------------------------------------------------
CELL_SIZE = 24
GRID_WIDTH = 30
GRID_HEIGHT = 20
HUD_HEIGHT = 44
WINDOW_WIDTH = CELL_SIZE * GRID_WIDTH      # 720 px
WINDOW_HEIGHT = CELL_SIZE * GRID_HEIGHT + HUD_HEIGHT  # 524 px
BOARD_OFFSET_Y = HUD_HEIGHT
WINDOW_TITLE = "Classic Snake - ChatDev"
# Main-loop frame delay in milliseconds (~60 FPS rendering).
FRAME_DELAY_MS = 16
# ---------------------------------------------------------------------------
# Directions (dx, dy)
# ---------------------------------------------------------------------------
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)
# ---------------------------------------------------------------------------
# Application states
# ---------------------------------------------------------------------------
STATE_MENU = "MENU"
STATE_PLAYING = "PLAYING"
STATE_PAUSED = "PAUSED"
STATE_GAME_OVER = "GAME_OVER"
# ---------------------------------------------------------------------------
# Difficulty presets
# ---------------------------------------------------------------------------
DIFFICULTIES = {
    "Easy":   {"label": "Easy   - slow snake, relaxed pace",  "speed": 6,  "points": 10},
    "Medium": {"label": "Medium - classic speed",             "speed": 10, "points": 20},
    "Hard":   {"label": "Hard   - fast snake for experts",    "speed": 15, "points": 30},
}
DIFFICULTY_ORDER = ["Easy", "Medium", "Hard"]
# ---------------------------------------------------------------------------
# Colors (hex strings understood by tkinter)
# ---------------------------------------------------------------------------
COLOR_BACKGROUND = "#101018"
COLOR_GRID = "#1c1c28"
COLOR_BORDER = "#3a3a55"
COLOR_SNAKE_HEAD = "#7cf67c"
COLOR_SNAKE_BODY = "#3fae3f"
COLOR_SNAKE_BODY_ALT = "#35962f"
COLOR_FOOD = "#ff4d4d"
COLOR_TEXT = "#e8e8f0"
COLOR_TEXT_DIM = "#9a9ab0"
COLOR_HIGHLIGHT = "#ffd75e"
COLOR_OVERLAY = "#181824"