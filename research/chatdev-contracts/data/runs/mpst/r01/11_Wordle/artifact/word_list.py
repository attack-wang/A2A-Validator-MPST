'''
word_list.py
Word data for the terminal-based Wordle game.
ANSWER_WORDS  -- tuple of common 5-letter English words that can be the
                 hidden "word of the day" (the daily answer pool).
VALID_WORDS   -- frozenset of every 5-letter word accepted as a guess.
                 It is a superset of ANSWER_WORDS and also contains
                 additional legitimate English words (plurals, less
                 common vocabulary, etc.) so that players are not
                 unfairly rejected when guessing.
All words are lowercase and exactly 5 alphabetic characters long.
'''