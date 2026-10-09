'''
word_manager.py
...
'''
import datetime
import random
from word_list import ANSWER_WORDS, VALID_GUESS_WORDS
class WordManager:
    """Loads the word lists and provides daily-word selection and validation."""
    WORDLE_EPOCH = datetime.date(2021, 6, 19)  # day zero for the daily rotation
    def __init__(self, answer_words=None, valid_guess_words=None):
        self.answer_words = self._sanitize(answer_words or ANSWER_WORDS)
        self.valid_guess_words = self._sanitize(valid_guess_words or VALID_GUESS_WORDS)
        # every answer must also be a legal guess
        self.valid_guess_words = sorted(set(self.valid_guess_words) | set(self.answer_words))
        self._valid_set = set(self.valid_guess_words)
    @staticmethod
    def _sanitize(words):
        cleaned = set()
        for w in words:
            w = str(w).strip().lower()
            if len(w) == 5 and w.isalpha():
                cleaned.add(w)
        return sorted(cleaned)
    def get_daily_word(self, day=None):
        """Deterministically pick the word of the day for the given date."""
        if day is None:
            day = datetime.date.today()
        offset = (day - self.WORDLE_EPOCH).days
        index = offset % len(self.answer_words)
        return self.answer_words[index]
    def get_random_word(self):
        return random.choice(self.answer_words)
    def is_valid_guess(self, word):
        return word.lower() in self._valid_set
    @property
    def answer_count(self):
        return len(self.answer_words)
    @property
    def guess_count(self):
        return len(self.valid_guess_words)