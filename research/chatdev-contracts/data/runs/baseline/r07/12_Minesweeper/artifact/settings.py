'''
settings.py
Central configuration for the Minesweeper game.
Contains difficulty presets, layout dimensions, colors, and font settings
used across all other modules.
'''
# ---------------------------------------------------------------------------
# Difficulty presets: name -> (cols, rows, mines)
# Classic Minesweeper layouts.
# ---------------------------------------------------------------------------
DIFFICULTIES = {
    "Beginner": (9, 9, 10),
    "Intermediate": (16, 16, 40),
    "Expert": (30, 16, 99),
}
# Order in which difficulties appear on the menu screen.
DIFFICULTY_ORDER = ["Beginner", "Intermediate", "Expert"]
# ---------------------------------------------------------------------------
# Layout
# ---------------------------------------------------------------------------
CELL_SIZE = 32          # Pixel size of one cell (square).
HUD_HEIGHT = 64         # Height of the status bar (counters + smiley).
BOARD_MARGIN = 12       # Margin around the board / HUD.
FPS = 60
# ---------------------------------------------------------------------------
# Colors (R, G, B)
# ---------------------------------------------------------------------------
COLOR_BACKGROUND = (189, 189, 189)      # Light gray window background
COLOR_BOARD = (189, 189, 189)
COLOR_COVERED = (192, 192, 192)         # Classic silver for covered cells
COLOR_COVERED_LIGHT = (255, 255, 255)   # Bevel highlight
COLOR_COVERED_DARK = (128, 128, 128)    # Bevel shadow
COLOR_UNCOVERED = (189, 189, 189)       # Flat gray for revealed cells
COLOR_UNCOVERED_BORDER = (128, 128, 128)
COLOR_HUD = (192, 192, 192)
COLOR_BLACK = (0, 0, 0)
COLOR_WHITE = (255, 255, 255)
COLOR_RED = (255, 0, 0)
COLOR_DARK_RED = (139, 0, 0)
COLOR_LED_BG = (0, 0, 0)                # Counter background
COLOR_LED_DIGIT = (255, 0, 0)           # LED digits
COLOR_FLAG_POLE = (0, 0, 0)
COLOR_FLAG_BANNER = (255, 0, 0)
COLOR_MINE = (0, 0, 0)
COLOR_EXPLODED_BG = (255, 0, 0)         # Background of the mine that exploded
COLOR_WRONG_FLAG_X = (255, 0, 0)
COLOR_BUTTON = (192, 192, 192)
COLOR_BUTTON_HOVER = (169, 169, 169)
COLOR_TEXT = (0, 0, 0)
COLOR_TITLE = (0, 0, 139)
# Number colors for revealed adjacent-mine counts (1..8).
NUMBER_COLORS = {
    1: (0, 0, 255),
    2: (0, 128, 0),
    3: (255, 0, 0),
    4: (0, 0, 128),
    5: (128, 0, 0),
    6: (0, 128, 128),
    7: (0, 0, 0),
    8: (128, 128, 128),
}
# ---------------------------------------------------------------------------
# Game rules
# ---------------------------------------------------------------------------
MAX_TIMER = 999