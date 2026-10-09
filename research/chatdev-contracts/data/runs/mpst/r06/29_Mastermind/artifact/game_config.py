'''
game_config.py
Central configuration for the Mastermind game.
Defines the available game modes and their settings:
  * COLOR_MODE - the classic game: six colors, code length 4,
    duplicate symbols allowed, 10 attempts.
  * DIGIT_MODE - a numeric variant: digits 0-9, code length 4,
    duplicate symbols allowed, 10 attempts.
Each mode dictionary provides:
  symbols          - the valid symbols the player may guess
  code_length      - how many symbols the secret code contains
  allow_duplicates - whether symbols may repeat inside the secret code
  max_attempts     - how many guesses the player gets
'''
COLOR_MODE = "colors"
DIGIT_MODE = "digits"
GAME_MODES = {
    COLOR_MODE: {
        "symbols": ["red", "orange", "yellow", "green", "blue", "purple"],
        "code_length": 4,
        "allow_duplicates": True,
        "max_attempts": 10,
    },
    DIGIT_MODE: {
        "symbols": ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"],
        "code_length": 4,
        "allow_duplicates": True,
        "max_attempts": 10,
    },
}
def get_mode_settings(mode):
    """Return the settings dictionary for `mode`, raising if unknown."""
    if mode not in GAME_MODES:
        raise KeyError(f"Unknown game mode: {mode!r}")
    return GAME_MODES[mode]