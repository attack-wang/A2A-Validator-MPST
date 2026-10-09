'''
constants.py
Central configuration and shared data for the Mastermind game.
This module only defines plain data (palette, input aliases, difficulty
presets) consumed by every other module. Keep it free of game logic.
'''
# --- ANSI helpers -----------------------------------------------------
RESET = "\033[0m"
BOLD = "\033[1m"
# --- Color palette ----------------------------------------------------
COLORS = {
    "1": {"name": "Red",    "ansi": "\033[91m"},
    "2": {"name": "Green",  "ansi": "\033[92m"},
    "3": {"name": "Blue",   "ansi": "\033[94m"},
    "4": {"name": "Yellow", "ansi": "\033[93m"},
    "5": {"name": "Orange", "ansi": "\033[95m"},
    "6": {"name": "Purple", "ansi": "\033[35m"},
}
# --- Letter aliases ---------------------------------------------------
LETTER_TO_KEY = {
    "r": "1",
    "g": "2",
    "b": "3",
    "y": "4",
    "o": "5",
    "p": "6",
}
# --- Difficulty presets -----------------------------------------------
DIFFICULTIES = {
    "1": {"name": "Easy",   "code_length": 4, "color_count": 6,
          "max_attempts": 12, "allow_duplicates": False},
    "2": {"name": "Medium", "code_length": 4, "color_count": 6,
          "max_attempts": 10, "allow_duplicates": True},
    "3": {"name": "Hard",   "code_length": 5, "color_count": 6,
          "max_attempts": 10, "allow_duplicates": True},
}
DEFAULT_DIFFICULTY_KEY = "2"