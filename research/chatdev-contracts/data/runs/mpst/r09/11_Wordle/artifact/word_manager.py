'''
word_manager.py
Selects the deterministic "word of the day" and validates guesses
against the embedded dictionary.
'''
import datetime
import random
from word_list import ANSWER_WORDS, EXTRA_VALID_GUESSES, all_valid_words
# Epoch used to number daily puzzles (original Wordle launched June 2021).
PUZZLE_EPOCH = datetime.date(2021, 6, 19)
class WordManager:
    '''Provides daily word selection and guess validation.'''
    def __init__(self, answer_words=None, extra_valid_words=None):
        self._answer_words = list(answer_words) if answer_words is not None else list(ANSWER_WORDS)
        extra = list(extra_valid_words) if extra_valid_words is not None else list(EXTRA_VALID_GUESSES)
        self._valid_words = set(self._answer_words) | set(extra)
    @property
    def answer_words(self): return tuple(self._answer_words)
    @property
    def valid_words(self): return set(self._valid_words)
    def is_valid_guess(self, guess):
        '''True if `guess` is a known 5-letter word.'''
        return guess in self._valid_words
    def get_word_for_date(self, day):
        '''Deterministically pick the answer for a given calendar date.'''
        seed = day.toordinal()
        rng = random.Random(seed)
        return rng.choice(self._answer_words)
    def get_daily_word(self, today=None):
        '''The word of the day (defaults to today's date).'''
        day = today if today is not None else datetime.date.today()
        return self.get_word_for_date(day)
    @staticmethod
    def puzzle_number(day):
        '''1-based daily puzzle index since the Wordle epoch.'''
        return (day - PUZZLE_EPOCH).days + 1