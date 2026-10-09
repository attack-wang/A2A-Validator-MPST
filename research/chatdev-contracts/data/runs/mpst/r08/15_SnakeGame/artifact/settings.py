'''
settings.py
Central configuration for the Classic Snake game: window dimensions, grid
size, colors, fonts, difficulty presets and scoring rules. Every module
imports this file as `cfg`, so all tunable values live here.
'''
# --- Window / layout -------------------------------------------------------
SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480
HEADER_HEIGHT = 40          # HUD bar height at the top of the window
BOARD_TOP = HEADER_HEIGHT   # playfield starts right below the HUD bar
# --- Grid ------------------------------------------------------------------
CELL_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // CELL_SIZE                    # 32 cells wide
GRID_HEIGHT = (SCREEN_HEIGHT - BOARD_TOP) // CELL_SIZE    # 22 cells tall
# --- Game loop -------------------------------------------------------------
RENDER_FPS = 60             # rendering frame rate (game logic is time-based)
# --- Fonts -----------------------------------------------------------------
FONT_SIZE_HEADER = 22
FONT_SIZE_MENU = 32
FONT_SIZE_MESSAGE = 20
# --- Scoring ---------------------------------------------------------------
SCORE_PER_FOOD = 10
SCORE_MULTIPLIERS = {
    "Easy": 1,
    "Medium": 2,
    "Hard": 3,
}
# --- Difficulty presets (snake speed in moves per second) -------------------
DIFFICULTY_SETTINGS = {
    "Easy": 6,
    "Medium": 10,
    "Hard": 15,
}
DEFAULT_DIFFICULTY = "Medium"
# --- Colors (R, G, B) -------------------------------------------------------
COLOR_BACKGROUND = (18, 18, 24)
COLOR_TEXT = (230, 230, 230)
COLOR_TEXT_DIM = (150, 150, 160)
COLOR_MENU_HIGHLIGHT = (120, 220, 120)
COLOR_SNAKE_HEAD = (80, 220, 100)
COLOR_SNAKE_BODY = (50, 160, 80)
COLOR_FOOD = (220, 60, 60)
COLOR_GRID_LINE = (35, 35, 45)
COLOR_BOARD_BORDER = (90, 90, 110)
COLOR_OVERLAY = (0, 0, 0)