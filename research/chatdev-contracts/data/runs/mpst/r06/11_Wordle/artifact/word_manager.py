'''
word_manager.py
...
'''
import datetime
import random
from words_data import ANSWER_WORDS, VALID_WORDS
class WordManager:
    """Selects the daily answer word and validates player guesses."""
    def __init__(self, answer_words=None, valid_words=None):
        self._answer_words = tuple(answer_words) if answer_words else ANSWER_WORDS
        self._valid_words = set(valid_words) if valid_words else set(VALID_WORDS)
    def get_daily_word(self, date=None):
        date = date or datetime.date.today()
        # days since epoch as stable index
        epoch = datetime.date(2021, 6, 19)  # original Wordle launch date
        day_index = (date - epoch).days
        return self._answer_words[day_index % len(self._answer_words)]
    def get_random_word(self):
        return random.choice(self._answer_words)
    def is_valid_word(self, word):
        return word.lower() in self._valid_words
    @property
    def answer_count(self):
        return len(self._answer_words)