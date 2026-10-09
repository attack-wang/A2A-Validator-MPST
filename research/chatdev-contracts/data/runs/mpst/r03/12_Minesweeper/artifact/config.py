'''
config.py
Central configuration for the Minesweeper application.
Defines the difficulty presets, board geometry, colour palette and
font settings used by both the game logic and the graphical interface.
'''
# ---------------------------------------------------------------------------
# Difficulty presets (classic Minesweeper values)
# ---------------------------------------------------------------------------
DIFFICULTIES = {
    "Beginner":     {"rows": 9,  "cols": 9,  "mines": 10},
    "Intermediate": {"rows": 16, "cols": 16, "mines": 40},
    "Expert":       {"rows": 16, "cols": 30, "mines": 99},
}
DEFAULT_DIFFICULTY = "Beginner"
# ---------------------------------------------------------------------------
# Board geometry
# ---------------------------------------------------------------------------
CELL_SIZE = 26
CELL_GAP = 0
HEADER_HEIGHT = 46
BORDER_WIDTH = 8
# ---------------------------------------------------------------------------
# Colour palette (classic Windows-style silver theme)
# ---------------------------------------------------------------------------
COLORS = {
    "background":     "#BDBDBD",
    "panel":          "#BDBDBD",
    "covered":        "#BDBDBD",
    "revealed":       "#C8C8C8",
    "bevel_light":    "#FFFFFF",
    "bevel_dark":     "#7B7B7B",
    "border":         "#8A8A8A",
    "exploded":       "#E8483F",
    "flag_pole":      "#1A1A1A",
    "flag_cloth":     "#E03C1C",
    "flag_base":      "#1A1A1A",
    "mine_body":      "#1A1A1A",
    "mine_highlight": "#FFFFFF",
    "cross":          "#CC0000",
    "counter_bg":     "#000000",
    "counter_fg":     "#FF3B30",
    "text":           "#1A1A1A",
}
NUMBER_COLORS = {
    1: "#1D4ED8",
    2: "#15803D",
    3: "#DC2626",
    4: "#1E3A8A",
    5: "#7F1D1D",
    6: "#0F766E",
    7: "#111111",
    8: "#6B7280",
}
# ---------------------------------------------------------------------------
# Fonts
# ---------------------------------------------------------------------------
FONT_FAMILY = "Helvetica"
FONT_COUNTER = (FONT_FAMILY, 16, "bold")
FONT_FACE = (FONT_FAMILY, 18)
FONT_STATUS = (FONT_FAMILY, 9)
FONT_ABOUT = (FONT_FAMILY, 10)
FONT_NUMBER = (FONT_FAMILY, 13, "bold")
FONT_LED = ("Courier", 16, "bold")
# Timer / counter limits
MAX_TIME = 999