'''
config.py
Configuration module for the Minesweeper game.
Defines the three difficulty presets (beginner, intermediate, expert)
and shared visual constants used by both the game logic and the GUI.
'''
from collections import namedtuple
Difficulty = namedtuple("Difficulty", ["name", "rows", "cols", "mines"])
BEGINNER = Difficulty("Beginner", 9, 9, 10)
INTERMEDIATE = Difficulty("Intermediate", 16, 16, 40)
EXPERT = Difficulty("Expert", 16, 30, 99)
DIFFICULTY_LEVELS = [BEGINNER, INTERMEDIATE, EXPERT]
# Colors for the numbers 1-8 displayed on revealed cells
NUMBER_COLORS = {
    1: "#0000FF",  # blue
    2: "#008000",  # green
    3: "#FF0000",  # red
    4: "#000080",  # dark blue
    5: "#800000",  # maroon
    6: "#008080",  # teal
    7: "#000000",  # black
    8: "#808080",  # gray
}
# Visual styles
UNREVEALED_BG = "#C0C0C0"      # classic gray
UNREVEALED_BORDER = "#FFFFFF"  # light border for raised 3D look
REVEALED_BG = "#E0E0E0"        # lighter gray for revealed cells
FLAGGED_BG = "#FFD966"         # distinct golden background for flagged cells
MINE_BG = "#FF4444"            # red background for exploded/revealed mines
WRONG_FLAG_BG = "#D0D0D0"      # background for wrongly flagged cells at game over
STATUS_BG = "#C0C0C0"          # status bar background
COUNTER_BG = "#000000"         # digital counter background
COUNTER_FG = "#FF0000"         # digital counter foreground (classic red LED)
# Geometry / fonts
CELL_SIZE = 32
CELL_FONT = ("Arial", 14, "bold")
STATUS_FONT = ("Consolas", 18, "bold")
FACE_FONT = ("Segoe UI Emoji", 14)