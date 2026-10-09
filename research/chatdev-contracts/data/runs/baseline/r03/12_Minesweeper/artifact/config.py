'''
Configuration module for the Minesweeper game.
Defines the difficulty presets, visual constants (colors, fonts, symbols)
and timing settings used across the whole application.
'''
# ---------------------------------------------------------------------------
# Difficulty presets
# ---------------------------------------------------------------------------
# Each difficulty maps to a tuple: (rows, cols, number_of_mines)
DIFFICULTIES = {
    "Beginner": (9, 9, 10),
    "Intermediate": (16, 16, 40),
    "Expert": (16, 30, 99),
}
DEFAULT_DIFFICULTY = "Beginner"
# ---------------------------------------------------------------------------
# Board / cell appearance
# ---------------------------------------------------------------------------
CELL_SIZE = 32              # pixel size of each cell button
FONT_FAMILY = "Helvetica"
FONT_CELL = (FONT_FAMILY, 12, "bold")
FONT_STATUS = (FONT_FAMILY, 12, "bold")
FONT_TITLE = (FONT_FAMILY, 14, "bold")
# Colors
COLOR_HIDDEN = "#BDBDBD"        # unrevealed cell background
COLOR_HIDDEN_ACTIVE = "#D6D6D6" # unrevealed cell on hover/active
COLOR_REVEALED = "#E8E8E8"      # revealed empty cell background
COLOR_FLAGGED = "#FFD966"       # flagged cell background (distinct visual)
COLOR_MINE_BG = "#E57373"       # background of the mine that exploded
COLOR_MINE_REVEALED = "#CFCFCF" # background of other mines at game over
COLOR_WRONG_FLAG_BG = "#FF8A80" # background of wrongly flagged cells
COLOR_BOARD_BG = "#9E9E9E"      # board frame background
COLOR_STATUS_BG = "#3C3F41"     # status bar background
COLOR_STATUS_FG = "#FFFFFF"     # status bar foreground
# Number colors (classic Minesweeper palette)
NUMBER_COLORS = {
    1: "#1976D2",  # blue
    2: "#388E3C",  # green
    3: "#D32F2F",  # red
    4: "#512DA8",  # purple
    5: "#8D6E63",  # brown
    6: "#0097A7",  # cyan
    7: "#212121",  # black
    8: "#757575",  # gray
}
# Symbols used on cells
SYMBOL_FLAG = "🚩"    # flag marker
SYMBOL_MINE = "💣"    # mine marker
SYMBOL_WRONG = "❌"   # wrongly flagged cell marker
# Smiley button states
SMILE_PLAYING = "🙂"
SMILE_WIN = "😎"
SMILE_LOSE = "😵"
SMILE_OH = "😮"       # shown while mouse pressed on a hidden cell
# Timer / status
TIMER_INTERVAL_MS = 1000
MAX_TIME_SECONDS = 999