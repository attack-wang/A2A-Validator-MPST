'''
config.py
Central configuration for the Mastermind game: color palette definitions,
feedback peg symbols, and difficulty presets.
The palette letters are the initials of the color names and are what the
player types when submitting a guess (e.g. "R G B Y" or "RGBY").
'''
from dataclasses import dataclass
# ---------------------------------------------------------------------------
# Feedback peg symbols
# ---------------------------------------------------------------------------
EXACT_PEG = "●"    # right color in the right position  (classic "black peg")
PARTIAL_PEG = "○"  # right color in the wrong position  (classic "white peg")
EMPTY_PEG = "·"    # unused feedback slot
# ---------------------------------------------------------------------------
# Color palette
# ---------------------------------------------------------------------------
# The first `palette_size` entries of this list are used for a given
# difficulty, so the palette grows with difficulty.
COLOR_NAMES = ["Red", "Green", "Blue", "Yellow", "Orange", "Purple", "Cyan", "Magenta"]
COLOR_LETTERS = [name[0].upper() for name in COLOR_NAMES]
# ANSI color codes used by ui.py to tint each palette letter.
# Values are SGR parameter strings (e.g. "31" = red, "38;5;208" = 256-color orange).
COLOR_ANSI = {
    "R": "31",        # Red
    "G": "32",        # Green
    "B": "34",        # Blue
    "Y": "33",        # Yellow
    "O": "38;5;208",  # Orange
    "P": "38;5;201",  # Purple
    "C": "36",        # Cyan
    "M": "35",        # Magenta
}
@dataclass(frozen=True)
class Difficulty:
    """Immutable description of one difficulty preset."""
    name: str
    code_length: int        # number of pegs in the secret code
    palette_size: int       # how many distinct colors are available
    max_attempts: int       # guesses allowed before losing
    allow_duplicates: bool  # may the secret contain the same color twice?
DIFFICULTIES = {
    "1": Difficulty(name="Easy",    code_length=4, palette_size=4, max_attempts=12, allow_duplicates=False),
    "2": Difficulty(name="Classic", code_length=4, palette_size=6, max_attempts=12, allow_duplicates=True),
    "3": Difficulty(name="Hard",    code_length=5, palette_size=8, max_attempts=10, allow_duplicates=True),
}
DEFAULT_DIFFICULTY_KEY = "2"
QUIT_COMMANDS = {"q", "quit", "exit"}