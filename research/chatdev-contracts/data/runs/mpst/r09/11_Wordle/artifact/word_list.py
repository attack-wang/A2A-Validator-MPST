'''
word_list.py
Embedded English word lists for the terminal Wordle game.
ANSWER_WORDS          -- common 5-letter words eligible as the daily answer.
EXTRA_VALID_GUESSES   -- additional 5-letter words accepted as guesses but
                         (mostly) never selected as the daily answer.
'''
ANSWER_WORDS = [ ... ]
EXTRA_VALID_GUESSES = [ ... ]
def all_valid_words():
    return set(ANSWER_WORDS) | set(EXTRA_VALID_GUESSES)