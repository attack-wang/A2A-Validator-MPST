'''
config.py
Central configuration for the Mastermind game.
Defines the difficulty presets, the default difficulty, the master
color palette, and the symbols used to render feedback pegs.
'''
# Master palette: the first `palette_size` colors are active per round.
# First letters must stay unique (R, G, B, Y, O, P, C, M, W).
PALETTE = [
    "Red", "Green", "Blue", "Yellow",
    "Orange", "Purple", "Cyan", "Magenta", "White",
]
DIFFICULTIES = {
    "1": {"name": "Easy", "code_length": 4, "palette_size": 4, "max_attempts": 12},
    "2": {"name": "Medium", "code_length": 4, "palette_size": 6, "max_attempts": 10},
    "3": {"name": "Hard", "code_length": 5, "palette_size": 7, "max_attempts": 10},
}
DEFAULT_DIFFICULTY = "2"
EXACT_SYMBOL = "●"
PARTIAL_SYMBOL = "○"
EMPTY_SYMBOL = "·"