'''
word_manager.py
'''
import datetime
import random
from word_list import WORD_LIST
class WordManager:
    EPOCH = datetime.date(2021, 6, 19)  # original Wordle launch date
    def __init__(self, words=None):
        raw = words if words is not None else WORD_LIST
        # normalize: lowercase, alphabetic, exactly 5 letters, dedupe, sort
        seen = set()
        cleaned = []
        for w in raw:
            w = str(w).strip().lower()
            if len(w) == 5 and w.isalpha() and w not in seen:
                seen.add(w)
                cleaned.append(w)
        self.words = sorted(cleaned)
    def __len__(self): return len(self.words)
    def get_daily_word(self, today=None):
        today = today or datetime.date.today()
        days_since = (today - self.EPOCH).days
        index = days_since % len(self.words)
        return self.words[index]
    def get_random_word(self):
        return random.choice(self.words)
    def is_valid_word(self, word):
        return word.lower() in self.words