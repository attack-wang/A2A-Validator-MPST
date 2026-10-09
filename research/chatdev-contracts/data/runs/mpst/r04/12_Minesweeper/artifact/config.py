'''
config.py
Central configuration for the Minesweeper game: difficulty presets,
cell dimensions, and the classic color scheme for number hints.
'''
DIFFICULTY_SETTINGS = {
    "Beginner": {"rows": 9, "cols": 9, "mines": 10},
    "Intermediate": {"rows": 16, "cols": 16, "mines": 40},
    "Expert": {"rows": 16, "cols": 30, "mines": 99},
}
CELL_SIZE = 30
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