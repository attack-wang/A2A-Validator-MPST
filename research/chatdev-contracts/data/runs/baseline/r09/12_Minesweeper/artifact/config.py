'''
config.py
Configuration module for the Minesweeper game.
Defines the difficulty presets (board size, mine count and cell font size)
as well as the visual constants (colors, symbols) shared by the GUI.
'''
# Difficulty presets: each entry maps a difficulty name to its board
# dimensions, number of mines and the font size used to render cells.
DIFFICULTY_SETTINGS = {
    "Beginner": {"width": 9, "height": 9, "mines": 10, "font_size": 13},
    "Intermediate": {"width": 16, "height": 16, "mines": 40, "font_size": 12},
    "Expert": {"width": 30, "height": 16, "mines": 99, "font_size": 10},
}
# Difficulty used when the application starts.
DEFAULT_DIFFICULTY = "Beginner"
# Classic Minesweeper number colors (1-8 adjacent mines).
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
# Visual appearance constants.
UNREVEALED_BG = "#C0C0C0"   # classic gray for covered cells
REVEALED_BG = "#D9D9D9"     # lighter gray for uncovered cells
EXPLODED_BG = "#FF0000"     # red highlight for the mine that was hit
STATUS_BG = "#C0C0C0"       # status bar background
COUNTER_FG = "#FF0000"      # LED-style red digits
COUNTER_BG = "#000000"      # LED-style black background
# Symbols displayed on cells.
FLAG_SYMBOL = "🚩"
MINE_SYMBOL = "💣"
WRONG_FLAG_SYMBOL = "❌"
# Faces shown on the reset button.
FACE_SMILE = "🙂"
FACE_WIN = "😎"
FACE_DEAD = "😵"
# Timer / counter limits (classic 3-digit LED displays).
MAX_DISPLAY_TIME = 999