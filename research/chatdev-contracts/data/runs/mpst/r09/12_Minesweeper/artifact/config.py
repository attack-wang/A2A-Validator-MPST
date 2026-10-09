"""
Configuration module for the Minesweeper game.
Defines the three difficulty presets (board dimensions and mine counts)
together with the visual constants (colors and symbols) used by the GUI.
"""
from collections import namedtuple
Difficulty = namedtuple("Difficulty", ["name", "rows", "cols", "mines"])
BEGINNER = Difficulty("Beginner", 9, 9, 10)
INTERMEDIATE = Difficulty("Intermediate", 16, 16, 40)
EXPERT = Difficulty("Expert", 16, 30, 99)
DIFFICULTY_LEVELS = [BEGINNER, INTERMEDIATE, EXPERT]
DEFAULT_DIFFICULTY = BEGINNER
CELL_SIZE = 30
FONT_CELL = ("Helvetica", 12, "bold")
FONT_HEADER = ("Helvetica", 14, "bold")
FONT_TITLE = ("Helvetica", 11)
COLOR_BG = "#BDBDBD"          # classic light-gray board background
COLOR_UNREVEALED = "#C0C0C0"  # raised cell face
COLOR_REVEALED = "#D6D6D6"    # sunken cell face
COLOR_FLAG_BG = "#FFE082"     # distinct amber background for flagged cells
COLOR_MINE_BG = "#E57373"     # red highlight for the mine that lost the game
COLOR_HEADER_BG = "#B0B0B0"
NUMBER_COLORS = {
    1: "#0000FF",
    2: "#008000",
    3: "#FF0000",
    4: "#000080",
    5: "#800000",
    6: "#008080",
    7: "#000000",
    8: "#696969",
}
FLAG_SYMBOL = "🚩"
MINE_SYMBOL = "💣"
WRONG_FLAG_SYMBOL = "❌"
FACE_PLAYING = "🙂"
FACE_WIN = "😎"
FACE_LOSE = "😵"