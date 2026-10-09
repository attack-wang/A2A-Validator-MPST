'''
wordlist.py
Manages the game's vocabulary: built-in answer words and valid guess words,
with support for optional external word list files, and deterministic
"daily word" selection based on the current date.
'''
import os
import hashlib
from datetime import date
from word_data import ANSWER_WORDS, EXTRA_VALID_GUESSES
class WordListManager:
    def __init__(self, answers_file=None, guesses_file=None):
        self.answers = set(ANSWER_WORDS)
        self.valid_guesses = set(ANSWER_WORDS) | set(EXTRA_VALID_GUESSES)
        # optionally load external files to extend lists
        ...
    def get_daily_word(self, day=None):
        day = day or date.today()
        key = day.isoformat().encode()
        index = int(hashlib.sha256(key).hexdigest(), 16) % len(sorted_answers)
        return sorted_answers[index]
    def is_valid_word(self, word):
        return word in self.valid_guesses