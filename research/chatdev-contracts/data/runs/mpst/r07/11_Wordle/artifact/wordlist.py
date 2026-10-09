'''
wordlist.py
Word-list loading and word-of-the-day selection.
Loads 5-letter English words from words.txt (one or more per line,
whitespace separated). If the file is missing, falls back to a small
built-in list so the game still runs.
The daily word is chosen deterministically from the calendar date
(same word for everyone on the same day, like the original Wordle),
while practice mode picks a uniformly random word.
'''
import random
from datetime import date
WORD_LENGTH = 5
DEFAULT_WORD_FILE = "words.txt"
# Minimal fallback used only when words.txt cannot be read.
FALLBACK_WORDS = [
    "CRANE", "CRATE", "TRACE", "SLATE", "PLANT", "MOUNT", "HOUSE", "MOUSE",
    "STARE", "SHARE", "FLAME", "GRAPE", "STONE", "BRAIN", "CLOUD", "DREAM",
    "LIGHT", "WATER", "SMILE", "HEART", "TIGER", "LEMON", "BREAD", "CHAIR",
]
class WordProvider:
    """Loads the dictionary and provides daily / random target words."""
    def __init__(self, path=DEFAULT_WORD_FILE):
        self.path = path
        self.words = self._load_words()
        self._word_set = set(self.words)
    def _load_words(self):
        """Read words.txt, keeping only clean 5-letter alphabetic words."""
        words = []
        try:
            with open(self.path, "r", encoding="utf-8") as handle:
                for line in handle:
                    for token in line.split():
                        word = token.strip().upper()
                        if len(word) == WORD_LENGTH and word.isalpha():
                            words.append(word)
        except FileNotFoundError:
            words = list(FALLBACK_WORDS)
        # De-duplicate while preserving order.
        seen = set()
        unique = []
        for word in words:
            if word not in seen:
                seen.add(word)
                unique.append(word)
        if not unique:
            raise RuntimeError("No valid 5-letter words available to play.")
        return unique
    def get_daily_word(self):
        """Deterministic word of the day, seeded by the calendar date."""
        today = date.today()
        day_seed = today.toordinal()  # stable, monotonic day counter
        rng = random.Random(day_seed)
        return rng.choice(self.words)
    def get_random_word(self):
        """Uniformly random word for practice games."""
        return random.choice(self.words)
    def is_known_word(self, word):
        """True if `word` (any case) is part of the loaded dictionary."""
        return word.upper() in self._word_set