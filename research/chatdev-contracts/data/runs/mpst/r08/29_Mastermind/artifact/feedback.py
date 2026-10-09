'''
feedback.py
Pure scoring logic for Mastermind.
Implements the classic black-and-white peg evaluation:
  * black pegs  -> exact matches (right color in the right position)
  * white pegs  -> partial matches (right color in the wrong position)
The function is side-effect free so it can be unit tested in isolation.
'''
from collections import Counter
def calculate_feedback(guess, secret):
    '''
    Compare a guess against the secret code.
    ...
    '''
    if len(guess) != len(secret):
        raise ValueError('Guess and secret must have the same length.')
    exact = sum(1 for g, s in zip(guess, secret) if g == s)
    guess_counts = Counter(guess)
    secret_counts = Counter(secret)
    total_overlap = sum(min(guess_counts[color], secret_counts[color])
                        for color in guess_counts)
    partial = total_overlap - exact
    return exact, partial