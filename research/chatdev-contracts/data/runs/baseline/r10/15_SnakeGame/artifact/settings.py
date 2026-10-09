'''
settings.py
Global configuration constants for the Classic Snake game.
Changing values here (grid size, colors, difficulty speeds, etc.)
tweaks the whole game without touching the logic modules.
'''
# ---------------------------------------------------------------------------
# Grid / window configuration
# ---------------------------------------------------------------------------
CELL_SIZE = 30          # Pixels per grid cell
GRID_WIDTH = 20         # Number of cells horizontally
GRID_HEIGHT = 20        # Number of cells vertically
HUD_HEIGHT = 60         # Top bar height used for score / status display
WINDOW_WIDTH = CELL_SIZE * GRID_WIDTH                  # 600 px
WINDOW_HEIGHT = CELL_SIZE * GRID_HEIGHT + HUD_HEIGHT   # playfield + HUD
FPS_CAP = 60            # Rendering frame rate (logic speed is separate)
# ---------------------------------------------------------------------------
# Colors (R, G, B)
# ---------------------------------------------------------------------------
COLOR_BACKGROUND     = (18, 18, 18)
COLOR_GRID_LINE      = (32, 32, 32)
COLOR_BORDER         = (90, 90, 90)
COLOR_SNAKE_HEAD     = (0, 220, 80)
COLOR_SNAKE_BODY     = (0, 160, 60)
COLOR_SNAKE_BODY_ALT = (0, 140, 55)
COLOR_FOOD           = (230, 60, 60)
COLOR_TEXT           = (235, 235, 235)
COLOR_TEXT_DIM       = (150, 150, 150)
COLOR_TEXT_ACCENT    = (255, 210, 70)
COLOR_MENU_BG        = (12, 12, 28)
COLOR_OVERLAY        = (0, 0, 0, 180)   # RGBA overlay for pause / game over
# ---------------------------------------------------------------------------
# Gameplay configuration
# ---------------------------------------------------------------------------
SCORE_PER_FOOD = 10                       # Points awarded per food eaten
# Difficulty levels: name -> base moves per second
DIFFICULTY_LEVELS = {
    "Easy":   6,
    "Medium": 10,
    "Hard":   15,
}
# Progressive speed-up: every N foods eaten the speed grows a little
SPEED_UP_EVERY = 5      # foods per speed increase
SPEED_UP_STEP = 1       # extra moves per second per step
MAX_SPEED = 20          # upper bound for moves per second
# ---------------------------------------------------------------------------
# Directions (grid deltas)
# ---------------------------------------------------------------------------
UP    = (0, -1)
DOWN  = (0, 1)
LEFT  = (-1, 0)
RIGHT = (1, 0)
# ---------------------------------------------------------------------------
# Files
# ---------------------------------------------------------------------------
HIGHSCORE_FILE = "highscore.json"