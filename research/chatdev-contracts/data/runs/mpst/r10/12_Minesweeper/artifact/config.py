'''
config.py
Central configuration for the Minesweeper game.
Defines the three difficulty levels (beginner, intermediate, expert)
with their board dimensions and mine counts, as well as all visual
constants (cell size, colors, fonts) used by the GUI layer.
'''
# Difficulty presets: (rows, cols, mines)
DIFFICULTIES = {
    "Beginner":     {"rows": 9,  "cols": 9,  "mines": 10},
    "Intermediate": {"rows": 16, "cols": 16, "mines": 40},
    "Expert":       {"rows": 16, "cols": 30, "mines": 99},
}
DEFAULT_DIFFICULTY = "Beginner"
# --- Visual constants -----------------------------------------------------
CELL_SIZE = 32          # Pixel size of one cell
STATUS_HEIGHT = 48      # Height of the status bar (counter / face / timer)
PADDING = 8             # Outer padding around the board
# Colors
BG_COLOR = "#BDBDBD"          # Window / frame background
CELL_HIDDEN_FILL = "#C6C6C6"  # Unrevealed cell face
CELL_HIDDEN_LIGHT = "#FFFFFF" # Unrevealed cell highlight
CELL_HIDDEN_DARK = "#7B7B7B"  # Unrevealed cell shadow
CELL_REVEALED_FILL = "#E0E0E0" # Revealed cell face
CELL_REVEALED_BORDER = "#A0A0A0"
FLAG_COLOR = "#D32F2F"        # Flag body
FLAG_POLE_COLOR = "#3E2723"   # Flag pole
MINE_COLOR = "#212121"        # Mine body
MINE_BG_COLOR = "#E53935"     # Background of the cell that exploded
WRONG_FLAG_COLOR = "#8E24AA"  # Cross drawn over wrongly flagged cells
# Number colors (1..8), classic Minesweeper palette
NUMBER_COLORS = {
    1: "#1976D2",  # blue
    2: "#388E3C",  # green
    3: "#D32F2F",  # red
    4: "#512DA8",  # purple / dark blue
    5: "#7B1FA2",  # maroon-ish
    6: "#00897B",  # teal
    7: "#212121",  # black
    8: "#757575",  # gray
}
FONT_FAMILY = "Helvetica"
FONT_NUMBERS = (FONT_FAMILY, 14, "bold")
FONT_STATUS = (FONT_FAMILY, 16, "bold")
FONT_MENU = (FONT_FAMILY, 10)