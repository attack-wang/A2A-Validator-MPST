'''
config.py
Configuration module for the Minesweeper game.
Defines difficulty presets, visual constants (colors, sizes) and
game-state identifiers shared across the application.
'''
# Difficulty presets: (rows, cols, num_mines)
DIFFICULTIES = {
    "Beginner": {"rows": 9, "cols": 9, "mines": 10},
    "Intermediate": {"rows": 16, "cols": 16, "mines": 40},
    "Expert": {"rows": 16, "cols": 30, "mines": 99},
}
DEFAULT_DIFFICULTY = "Beginner"
# Game states
STATE_READY = "ready"
STATE_PLAYING = "playing"
STATE_WON = "won"
STATE_LOST = "lost"
# Face button captions
FACE_PLAYING = "\U0001F642"
FACE_WON = "\U0001F60E"
FACE_LOST = "\U0001F635"
# GUI geometry
CELL_SIZE = 32
CANVAS_PADDING = 8
# Colors
BG_COLOR = "#c0c0c0"
BOARD_BG = "#808080"
UNREVEALED_BG = "#c0c0c0"
REVEALED_BG = "#d9d9d9"
BEVEL_LIGHT = "#ffffff"
BEVEL_DARK = "#808080"
NUMBER_COLORS = {
    1: "#0000ff",
    2: "#008000",
    3: "#ff0000",
    4: "#000080",
    5: "#800000",
    6: "#008080",
    7: "#000000",
    8: "#808080",
}
MINE_FG = "#000000"
EXPLODED_BG = "#ff0000"
FLAG_POLE = "#000000"
FLAG_BODY = "#ff0000"
WRONG_FLAG_X = "#ff0000"
COUNTER_BG = "#000000"
COUNTER_FG = "#ff0000"
# Fonts
FONT_HEADER = ("Arial", 14, "bold")
FONT_CELL = ("Arial", 13, "bold")