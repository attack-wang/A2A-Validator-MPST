'''
config.py
Central configuration for the Mastermind game.
Defines the Difficulty presets (code length, palette size, attempt limit,
duplicate policy) and default game settings. Keeping these values in one
module makes it easy to tweak game balance without touching game logic.
'''
from dataclasses import dataclass
@dataclass(frozen=True)
class Difficulty:
    """Immutable description of one difficulty preset."""
    name: str
    code_length: int        # number of pegs in the secret code
    palette_size: int       # number of available colors
    max_attempts: int       # guesses before the player loses
    allow_duplicates: bool  # may the secret reuse a color?
    description: str
DIFFICULTIES = {
    "1": Difficulty(
        name="Easy",
        code_length=4,
        palette_size=6,
        max_attempts=12,
        allow_duplicates=True,
        description="4 pegs, 6 colors, 12 attempts (classic Mastermind)",
    ),
    "2": Difficulty(
        name="Medium",
        code_length=4,
        palette_size=7,
        max_attempts=10,
        allow_duplicates=True,
        description="4 pegs, 7 colors, 10 attempts",
    ),
    "3": Difficulty(
        name="Hard",
        code_length=5,
        palette_size=8,
        max_attempts=10,
        allow_duplicates=True,
        description="5 pegs, 8 colors, 10 attempts",
    ),
    "4": Difficulty(
        name="Expert",
        code_length=6,
        palette_size=8,
        max_attempts=12,
        allow_duplicates=False,
        description="6 pegs, 8 colors, 12 attempts, no repeated colors",
    ),
}
DEFAULT_DIFFICULTY_KEY = "1"
# Commands the player can type instead of a guess.
COMMAND_HELP = "help"
COMMAND_QUIT = "quit"