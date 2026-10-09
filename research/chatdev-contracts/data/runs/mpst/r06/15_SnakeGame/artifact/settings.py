'''
settings.py
Central configuration for the Snake game: grid dimensions, colors,
scoring rules, and difficulty level definitions (snake speed per level).
'''
# ---------------------------------------------------------------------------
# Grid / window configuration
# ---------------------------------------------------------------------------
CELL_SIZE = 20                       # Pixel size of a single grid cell
GRID_WIDTH = 30                      # Playable cells horizontally
GRID_HEIGHT = 20                     # Playable cells vertically
SCREEN_WIDTH = CELL_SIZE * GRID_WIDTH
SCREEN_HEIGHT = CELL_SIZE * GRID_HEIGHT
UI_BAR_HEIGHT = 40                   # Top bar height (score display)
WINDOW_HEIGHT = SCREEN_HEIGHT + UI_BAR_HEIGHT
RENDER_FPS = 60                      # Rendering frame rate
# ---------------------------------------------------------------------------
# Colors (R, G, B)
# ---------------------------------------------------------------------------
COLOR_BACKGROUND = (18, 18, 18)
COLOR_GRID_LINE = (32, 32, 32)
COLOR_UI_BAR = (35, 35, 45)
COLOR_SNAKE_HEAD = (0, 220, 100)
COLOR_SNAKE_BODY = (0, 160, 70)
COLOR_FOOD = (230, 60, 60)
COLOR_TEXT = (235, 235, 235)
COLOR_TEXT_DIM = (150, 150, 150)
COLOR_HIGHLIGHT = (255, 210, 60)
# ---------------------------------------------------------------------------
# Scoring
# ---------------------------------------------------------------------------
SCORE_PER_FOOD = 10                  # Points awarded for each food eaten
# ---------------------------------------------------------------------------
# Difficulty levels: name -> snake moves per second
# ---------------------------------------------------------------------------
DIFFICULTIES = {
    "Easy": 6,
    "Medium": 10,
    "Hard": 15,
}