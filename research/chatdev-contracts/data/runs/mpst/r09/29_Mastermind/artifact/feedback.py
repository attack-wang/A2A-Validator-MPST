'''
feedback.py
Computation of Mastermind feedback.
Implements the classic scoring rules: an "exact" peg for every guess
peg that matches the secret in both color and position, and a
"partial" peg for every remaining peg whose color exists in the secret
but sits in the wrong position. The multiset-based algorithm stays
correct even when the code contains duplicate colors.
'''
from collections import Counter
class Feedback:
    '''Immutable result of comparing one guess against the secret.'''
    def __init__(self, exact, partial):
        '''Store the number of exact and partial matches.'''
        self.exact = exact
        self.partial = partial
    def is_win(self, code_length):
        '''True when every position is an exact match.'''
        return self.exact == code_length
    def __eq__(self, other):
        if not isinstance(other, Feedback):
            return NotImplemented
        return (self.exact, self.partial) == (other.exact, other.partial)
    def __hash__(self):
        return hash((self.exact, self.partial))
    def __repr__(self):
        return f'Feedback(exact={self.exact}, partial={self.partial})'
def compute_feedback(guess, secret):
    '''Compare a guess to the secret; return a Feedback object.
    Exact matches are counted position by position first. Partial
    matches are then derived from the multiset intersection of both
    codes minus the exact matches, which correctly handles duplicates.
    '''
    exact = sum(1 for g, s in zip(guess, secret) if g == s)
    guess_counts = Counter(guess)
    secret_counts = Counter(secret)
    common = sum(
        min(count, secret_counts[color])
        for color, count in guess_counts.items()
    )
    partial = common - exact
    return Feedback(exact, partial)