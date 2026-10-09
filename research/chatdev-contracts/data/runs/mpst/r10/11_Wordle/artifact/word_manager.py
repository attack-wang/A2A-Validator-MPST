'''
word_manager.py
Selects the daily (or random) answer word and validates guesses against the dictionary.
'''
import datetime
import random
from words import ANSWER_WORDS, EXTRA_VALID_GUESSES
EPOCH = datetime.date(2021, 6, 19)  # original Wordle launch date, used for puzzle numbering
class WordManager:
    def __init__(self, answer_words=None, valid_words=None):
        self._answer_words = tuple(answer_words) if answer_words else ANSWER_WORDS
        extra = tuple(valid_words) if valid_words else EXTRA_VALID_GUESSES
        self._valid_words = frozenset(w.lower() for w in self._answer_words) | frozenset(w.lower() for w in extra)
    @property
    def puzzle_number(self):
        today = datetime.date.today()
        return (today - EPOCH).days
    def get_daily_word(self):
        seed = datetime.date.today().toordinal()
        rng = random.Random(seed)
        return rng.choice(self._answer_words)
    def get_word_for_date(self, day):
        rng = random.Random(day.toordinal())
        return rng.choice(self._answer_words)
    def get_random_word(self):
        return random.choice(self._answer_words)
    def is_valid_guess(self, word):
        return word in self._valid_words