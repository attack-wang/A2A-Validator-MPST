'''
word_manager.py
Loads word lists and provides daily word selection...
'''
import datetime
import random
from wordlists import ANSWER_WORDS, EXTRA_VALID_WORDS
class WordManager:
    def __init__(self):
        self.answers = [w for w in ANSWER_WORDS if len(w) == 5]
        extra = [w for w in EXTRA_VALID_WORDS if len(w) == 5]
        self.valid_guesses = set(self.answers) | set(extra)
    def get_daily_word(self, date=None):
        """Deterministic word for the given date (defaults to today)."""
        date = date or datetime.date.today()
        seed = date.isoformat()
        rng = random.Random(seed)
        return rng.choice(self.answers)
    def get_random_word(self):
        return random.choice(self.answers)
    def is_valid_guess(self, word):
        return word.lower() in self.valid_guesses