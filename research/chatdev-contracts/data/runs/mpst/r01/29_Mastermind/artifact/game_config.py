'''
game_config.py
Central configuration for the Mastermind game: palettes for the "colors" and
"digits" modes, difficulty presets, and helper accessors that resolve a
(mode, difficulty) pair into concrete game settings. Every palette entry uses
the unified schema {"label", "letter", "ansi"} so all modules share one data
contract.
'''
COLOR_PALETTE = [
    {"label": "Red", "letter": "R", "ansi": "\033[91m"},
    {"label": "Orange", "letter": "O", "ansi": "\033[38;5;208m"},
    {"label": "Yellow", "letter": "Y", "ansi": "\033[93m"},
    {"label": "Green", "letter": "G", "ansi": "\033[92m"},
    {"label": "Blue", "letter": "B", "ansi": "\033[94m"},
    {"label": "Purple", "letter": "P", "ansi": "\033[95m"},
    {"label": "Cyan", "letter": "C", "ansi": "\033[96m"},
    {"label": "Magenta", "letter": "M", "ansi": "\033[35m"},
    {"label": "White", "letter": "W", "ansi": "\033[97m"},
    {"label": "Black", "letter": "K", "ansi": "\033[90m"},
]
DIGIT_PALETTE = [
    {"label": "1", "letter": "1", "ansi": "\033[91m"},
    {"label": "2", "letter": "2", "ansi": "\033[93m"},
    {"label": "3", "letter": "3", "ansi": "\033[92m"},
    {"label": "4", "letter": "4", "ansi": "\033[96m"},
    {"label": "5", "letter": "5", "ansi": "\033[94m"},
    {"label": "6", "letter": "6", "ansi": "\033[95m"},
    {"label": "7", "letter": "7", "ansi": "\033[97m"},
    {"label": "8", "letter": "8", "ansi": "\033[90m"},
    {"label": "9", "letter": "9", "ansi": "\033[38;5;208m"},
    {"label": "0", "letter": "0", "ansi": "\033[36m"},
]
MODES = {"colors": COLOR_PALETTE, "digits": DIGIT_PALETTE}
DIFFICULTY_PRESETS = {
    "colors": {
        "easy": {"code_length": 4, "max_attempts": 12, "allow_duplicates": True},
        "medium": {"code_length": 4, "max_attempts": 10, "allow_duplicates": True},
        "hard": {"code_length": 5, "max_attempts": 10, "allow_duplicates": True},
    },
    "digits": {
        "easy": {"code_length": 4, "max_attempts": 12, "allow_duplicates": False},
        "medium": {"code_length": 4, "max_attempts": 10, "allow_duplicates": True},
        "hard": {"code_length": 6, "max_attempts": 10, "allow_duplicates": True},
    },
}
def resolve_settings(mode, difficulty):
    mode = mode.strip().lower()
    difficulty = difficulty.strip().lower()
    if mode not in MODES:
        raise ValueError(...)
    if difficulty not in DIFFICULTY_PRESETS[mode]:
        raise ValueError(...)
    settings = dict(DIFFICULTY_PRESETS[mode][difficulty])
    settings["palette"] = MODES[mode]
    settings["mode"] = mode
    settings["difficulty"] = difficulty
    return settings