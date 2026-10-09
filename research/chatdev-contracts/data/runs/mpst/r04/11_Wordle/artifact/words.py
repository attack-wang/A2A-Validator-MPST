'''Word list and daily word selection for the Wordle game.'''
import datetime
import random
WORD_LENGTH = 5
_RAW_WORDS = (
    "abide", "about", ...
)
WORDS = sorted(set(w for w in _RAW_WORDS if len(w) == WORD_LENGTH and w.isalpha()))