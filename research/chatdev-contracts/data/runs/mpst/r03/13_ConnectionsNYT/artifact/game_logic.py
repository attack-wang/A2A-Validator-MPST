"""
game_logic.py
Core game state and rules for the daily Connections word-grouping puzzle.
"""
import random
# Difficulty colors in reveal order (easiest -> hardest)
DIFFICULTY_ORDER = {"yellow": 0, "green": 1, "blue": 2, "purple": 3}
MAX_MISTAKES = 4
GROUP_SIZE = 4
class GuessResult:
    """Outcome of a submitted guess."""
    CORRECT = "correct"
    INCORRECT = "incorrect"
    ...
class ConnectionsGame:
    def __init__(self, puzzle):
        self.puzzle = puzzle
        self.grid_words = list(puzzle.initial_order)
        self.selected = []  # ordered list of selected words
        self.mistakes = 0
        self.found_groups = []  # list of category dicts in reveal order
        self.status = "playing"  # "playing", "won", "lost"
    def toggle_select(self, word): ...
    def clear_selection(self): ...
    def shuffle(self): ...
    def submit_guess(self) -> dict: ...
    def _one_away(self, words) -> bool: ...
    ...