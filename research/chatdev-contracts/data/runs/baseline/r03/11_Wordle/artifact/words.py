'''
words.py
Word list management for the Wordle game.
Provides:
- WORD_LIST: a curated list of common five-letter English words.
- load_words(): returns the list of valid guess words.
- get_daily_word(): deterministically selects the "word of the day" based
  on the current date, so every player gets the same word on a given day.
- is_valid_word(word): checks whether a guess is an acceptable word.
'''
import datetime
import random
# Curated list of common five-letter English words (answers & valid guesses)
WORD_LIST = [
    "about", "above", "abuse", "actor", "acute", "admit", "adopt", "adult",
    "after", "again", "agent", "agree", "ahead", "alarm", "album", "alert",
    ...
]