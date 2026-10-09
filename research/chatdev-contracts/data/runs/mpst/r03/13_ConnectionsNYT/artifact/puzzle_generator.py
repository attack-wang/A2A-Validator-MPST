"""
puzzle_generator.py
Generates the daily puzzle deterministically from the current date.
"""
import random
from datetime import date, timedelta
from puzzle_data import PUZZLE_POOL
class Puzzle:
    """Represents a single daily puzzle instance."""
    def __init__(self, puzzle_id, categories, display_date):
        ...
    @property
    def all_words(self): ...
    def category_of(self, word): ...
    ...
EPOCH_START = date(2024, 1, 1)  # reference date for puzzle numbering
def get_puzzle_number(d: date) -> int:
    """Days since epoch start; puzzle #0 on the first day."""
    return (d - EPOCH_START).days
def get_daily_puzzle(d=None) -> Puzzle:
    """Return the deterministic puzzle for the given date (today by default)."""
    if d is None:
        d = date.today()
    number = get_puzzle_number(d)
    rng = random.Random(f"connections-{d.isoformat()}")
    index = number % len(PUZZLE_POOL)
    definition = PUZZLE_POOL[index]
    categories = [dict(c) for c in definition["categories"]]
    # Deterministic shuffle of display order
    words = [w for c in categories for w in c["words"]]
    rng.shuffle(words)  # hmm, need to shuffle into 4x4 grid order
    ...