'''
config.py
Central configuration for the Minesweeper game...
'''
# ----------------------------------------------------------------------
# Difficulty presets: (cols, rows, mines) - classic Windows Minesweeper
# ----------------------------------------------------------------------
DIFFICULTIES = {
    "beginner":     {"cols": 9,  "rows": 9,  "mines": 10},
    "intermediate": {"cols": 16, "rows": 16, "mines": 40},
    "expert":       {"cols": 30, "rows": 16, "mines": 99},
}
DIFFICULTY_ORDER = ["beginner", "intermediate", "expert"]
# ----------------------------------------------------------------------
# Layout
# ----------------------------------------------------------------------
CELL_SIZE = 32
BOARD_MARGIN = 10
HEADER_HEIGHT = 72
MENU_WIDTH = 640
MENU_HEIGHT = 480
def game_window_size(cols, rows):
    """Total window size needed for a board of the given dimensions."""
    width = BOARD_MARGIN * 2 + cols * CELL_SIZE
    height = HEADER_HEIGHT + BOARD_MARGIN * 2 + rows * CELL_SIZE
    return width, height
# ----------------------------------------------------------------------
# Fonts
# ----------------------------------------------------------------------
FONT_NAME = "arial"
FONT_TITLE_SIZE = 44
FONT_UI_SIZE = 18
FONT_COUNTER_SIZE = 28
FONT_NUMBER_SIZE = 18
FONT_OVERLAY_SIZE = 40
# ----------------------------------------------------------------------
# Colours (R, G, B)
# ----------------------------------------------------------------------
# General UI
COLOR_BACKGROUND = (45, 45, 48)
COLOR_PANEL = (189, 189, 189)
COLOR_PANEL_DARK = (160, 160, 160)
COLOR_BUTTON = (70, 70, 75)
COLOR_BUTTON_HOVER = (95, 95, 105)
COLOR_BUTTON_TEXT = (240, 240, 240)
COLOR_BEVEL_DARK = (35, 35, 38)
COLOR_BEVEL_LIGHT = (230, 230, 230)
# Cells
COLOR_CELL_HIDDEN = (170, 170, 175)
COLOR_CELL_HIDDEN_EDGE = (120, 120, 125)
COLOR_CELL_REVEALED = (215, 215, 215)
COLOR_CELL_REVEALED_EDGE = (150, 150, 150)
COLOR_CELL_EXPLODED = (230, 70, 60)
COLOR_MINE = (25, 25, 25)
COLOR_MINE_WRONG = (230, 70, 60)
# Number colours 1..8 (classic palette)
COLOR_NUMBERS = {
    1: (20, 60, 220),
    2: (20, 130, 30),
    3: (220, 40, 40),
    4: (20, 20, 130),
    5: (130, 20, 20),
    6: (20, 130, 130),
    7: (20, 20, 20),
    8: (120, 120, 120),
}
# Flag
COLOR_FLAG_POLE = (40, 40, 40)
COLOR_FLAG_CLOTH = (220, 50, 40)
# Smiley
COLOR_SMILEY = (255, 220, 60)
COLOR_SMILEY_BORDER = (180, 150, 20)
COLOR_SMILEY_EYE = (30, 30, 30)
# Timer / counter
COLOR_COUNTER_BG = (30, 30, 30)
COLOR_COUNTER_TEXT = (240, 60, 50)
# Overlay
COLOR_OVERLAY_WIN = (30, 140, 60)
COLOR_OVERLAY_LOSE = (180, 40, 40)
COLOR_OVERLAY_TEXT = (255, 255, 255)