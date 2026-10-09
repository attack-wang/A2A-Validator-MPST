'''
feedback.py
Feedback model and scoring for the Mastermind game.
Implements the classic Mastermind scoring rule:
* Exact matches ("black pegs"): a guessed color that matches the
  secret color in the very same position.
* Partial matches ("white pegs"): a guessed color that exists in the
  secret code but in a different position. Each secret color can be
  credited at most once, so duplicated colors are handled correctly.
'''
from collections import Counter
class Feedback:
    '''
    Value object describing the outcome of a single guess.
    Attributes:
        exact: number of positions where guess and secret agree
            (right color, right position) -- the "black pegs".
        partial: number of colors present in the secret but placed in
            the wrong position -- the "white pegs".
        total: length of the code, used to render empty peg slots and
            to decide whether the guess solved the code.
    '''
    def __init__(self, exact, partial, total):
        self.exact = exact
        self.partial = partial
        self.total = total
    @property
    def is_win(self):
        '''True when every position of the guess matches the secret.'''
        return self.exact == self.total
    def pegs(self, exact_peg, partial_peg, miss_peg):
        '''
        Return the feedback as a list of peg symbols, exact matches
        first, then partial matches, then empty slots.
        '''
        symbols = [exact_peg] * self.exact
        symbols += [partial_peg] * self.partial
        symbols += [miss_peg] * (self.total - self.exact - self.partial)
        return symbols
    def describe(self, exact_peg='*', partial_peg='o', miss_peg='-'):
        '''Human-readable one-line rendering, e.g. "* * o -". '''
        return ' '.join(self.pegs(exact_peg, partial_peg, miss_peg))
    def __repr__(self):
        return 'Feedback(exact=%d, partial=%d, total=%d)' % (
            self.exact, self.partial, self.total)
def compute_feedback(guess, secret):
    '''
    Score a guess against the secret code.
    Algorithm (classic Mastermind scoring):
      1. Walk both codes position by position; every position where
         guess[i] == secret[i] is an exact match and is removed from
         further consideration.
      2. For the remaining colors, count a partial match for every
         guess color that still has an unused counterpart in the
         secret (multiset intersection), so each secret color is
         credited at most once.
    Args:
        guess: list of color tokens submitted by the player.
        secret: list of color tokens of the hidden code.
    Returns:
        Feedback instance with exact/partial counts.
    Raises:
        ValueError: if guess and secret lengths differ.
    '''
    if len(guess) != len(secret):
        raise ValueError(
            'Guess length (%d) does not match secret length (%d).'
            % (len(guess), len(secret)))
    exact = 0
    guess_left = []
    secret_left = []
    for g, s in zip(guess, secret):
        if g == s:
            exact += 1
        else:
            guess_left.append(g)
            secret_left.append(s)
    available = Counter(secret_left)
    partial = 0
    for color in guess_left:
        if available[color] > 0:
            partial += 1
            available[color] -= 1
    return Feedback(exact, partial, len(secret))