'''
Daily word selection and dictionary management.
'''
import random
from datetime import date as _date
ANSWER_WORDS = [ ... ]
EXTRA_GUESS_WORDS = [ ... ]
class WordManager:
    def __init__(self, answers=None, valid_guesses=None):
        self.answers = list(answers) if answers is not None else ANSWER_WORDS
        if valid_guesses is None:
            valid_guesses = set(self.answers) | set(EXTRA_GUESS_WORDS)
        self.valid_guesses = set(valid_guesses)
        self.valid_guesses.update(w.lower() for w in self.answers)
    def daily_word(self, date=None):
        d = date if date is not None else _date.today()
        rng = random.Random(d.toordinal())
        return rng.choice(self.answers)
    def is_valid_guess(self, word):
        return word.lower() in self.valid_guesses