'''
config.py
Configuration module for the Minesweeper game.
Defines the difficulty presets (board size and mine count) used to
initialize a game session.
'''
from dataclasses import dataclass
@dataclass(frozen=True)
class GameConfig:
    """Immutable configuration describing a Minesweeper board."""
    name: str
    rows: int
    cols: int
    mines: int
# Classic Minesweeper difficulty presets.
BEGINNER = GameConfig(name="Beginner", rows=9, cols=9, mines=10)
INTERMEDIATE = GameConfig(name="Intermediate", rows=16, cols=16, mines=40)
EXPERT = GameConfig(name="Expert", rows=16, cols=30, mines=99)
DIFFICULTY_LEVELS = {
    "Beginner": BEGINNER,
    "Intermediate": INTERMEDIATE,
    "Expert": EXPERT,
}