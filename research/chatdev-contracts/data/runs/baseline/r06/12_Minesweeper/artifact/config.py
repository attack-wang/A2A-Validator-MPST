'''
Configuration constants for the Minesweeper game: difficulty presets, colors, fonts, sizes.
'''
# Difficulty presets: board size and mine count for each level.
DIFFICULTY_LEVELS = {
    "Beginner": {"rows": 9, "cols": 9, "mines": 10},
    "Intermediate": {"rows": 16, "cols": 16, "mines": 40},
    "Expert": {"rows": 16, "cols": 30, "mines": 99},
}
DIFFICULTY_ORDER = ["Beginner", "Intermediate", "Expert"]
DEFAULT_DIFFICULTY = "Beginner"
# Geometry
CELL_SIZE = 32
# Colors
COVERED_CELL_COLOR = "#c0c0c0"
REVEALED_CELL_COLOR = "#e3e3e3"
BEVEL_LIGHT = "#ffffff"
BEVEL_DARK = "#7b7b7b"
GRID_LINE_COLOR = "#a0a0a0"
EXPLOSION_COLOR = "#ff5a5a"
FLAG_COLOR = "#e02020"
FLAG_POLE_COLOR = "#333333"
MINE_COLOR = "#1a1a1a"
WRONG_FLAG_COLOR = "#cc0000"
NUMBER_COLORS = {
    1: "#1976d2",
    2: "#388e3c",
    3: "#d32f2f",
    4: "#000080",
    5: "#795548",
    6: "#0097a7",
    7: "#212121",
    8: "#757575",
}
# Fonts
CELL_NUMBER_FONT = ("Arial", 14, "bold")
HEADER_FONT = ("Arial", 16, "bold")
COUNTER_FONT = ("Courier", 16, "bold")