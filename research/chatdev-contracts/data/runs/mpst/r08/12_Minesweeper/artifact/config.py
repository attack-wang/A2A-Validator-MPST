'''
Configuration constants for the Minesweeper game.
Contains difficulty presets, visual styles, colors for adjacent-mine
numbers, and the symbols used for flags and mines.
'''
# Difficulty presets: difficulty name -> (rows, cols, number of mines)
DIFFICULTY_SETTINGS = {
    "Beginner": (9, 9, 10),
    "Intermediate": (16, 16, 40),
    "Expert": (16, 30, 99),
}
DEFAULT_DIFFICULTY = "Beginner"
# Cell button geometry and fonts
CELL_WIDTH = 3          # button width in text units
CELL_HEIGHT = 1         # button height in text units
CELL_MIN_SIZE = 28      # minimum cell size in pixels (grid slot)
FONT_MAIN = ("Helvetica", 12, "bold")
FONT_HEADER = ("Helvetica", 12, "bold")
# Classic Minesweeper colors for adjacent-mine counts 1-8
NUMBER_COLORS = {
    1: "#0000FF",  # blue
    2: "#008000",  # green
    3: "#FF0000",  # red
    4: "#000080",  # dark blue
    5: "#800000",  # dark red
    6: "#008080",  # teal
    7: "#000000",  # black
    8: "#808080",  # gray
}
# Cell visual styles
COVERED_BG = "#C8C8C8"      # covered cell background
REVEALED_BG = "#E8E8E8"     # revealed (safe) cell background
FLAG_BG = "#FFE08A"         # distinct background for flagged cells
FLAG_FG = "#B36B00"         # text color for the flag symbol
MINE_BG = "#B0B0B0"         # background for revealed mines
MINE_FG = "#000000"         # text color for mine symbols
EXPLODED_BG = "#FF5555"     # background for the mine that was clicked
EXPLODED_FG = "#FFFFFF"     # text color on the exploded mine
# Symbols displayed on special cells
FLAG_TEXT = "⚑"
MINE_TEXT = "●"
# Header/status text
COUNTER_FORMAT = "{:03d}"   # 3-digit display for mine counter and timer