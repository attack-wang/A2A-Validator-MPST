'''
feedback.py
Feedback calculation module for the Mastermind game.
Provides the core scoring logic that distinguishes between:
  * Exact matches  -- a guessed peg has the correct color AND is in the
                      correct position (traditionally shown as black pegs).
  * Partial matches -- a guessed peg has the correct color but is in the
                      wrong position (traditionally shown as white pegs).
The algorithm correctly handles duplicate colors so that a color in the
secret code is never counted more times than it actually appears.
'''
from collections import Counter
def calculate_feedback(secret, guess):
    '''
    Compare a guess against the secret code and produce Mastermind feedback.
    Args:
        secret (tuple/list): The hidden code, e.g. ('red', 'blue', ...).
        guess (tuple/list):  The player's guess of the same length.
    Returns:
        tuple: (exact_matches, partial_matches)
            exact_matches  (int): correct color AND correct position.
            partial_matches (int): correct color BUT wrong position.
    '''
    if len(secret) != len(guess):
        raise ValueError("Secret and guess must have the same length.")
    # --- Step 1: count exact matches (right color, right position) ---
    exact_matches = 0
    secret_remaining = Counter()
    guess_remaining = Counter()
    for s, g in zip(secret, guess):
        if s == g:
            exact_matches += 1
        else:
            # Keep track of unmatched colors for the partial-match pass.
            secret_remaining[s] += 1
            guess_remaining[g] += 1
    # --- Step 2: count partial matches (right color, wrong position) ---
    # For every color still present in both unmatched pools, the number of
    # partial matches is the overlap (minimum of the two counts).
    partial_matches = sum(
        min(count, guess_remaining[color])
        for color, count in secret_remaining.items()
    )
    return exact_matches, partial_matches