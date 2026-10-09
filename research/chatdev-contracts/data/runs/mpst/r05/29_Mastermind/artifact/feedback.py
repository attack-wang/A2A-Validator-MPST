'''
feedback.py
Guess evaluation for Mastermind.
Compares a guess against the secret code and produces a Feedback object
that distinguishes:
  * exact matches   - right color in the right position  ("black pegs")
  * partial matches - right color in the wrong position ("white pegs")
'''
from collections import Counter
from dataclasses import dataclass
@dataclass(frozen=True)
class Feedback:
    """Outcome of a single guess, in classic Mastermind peg terms."""
    exact_matches: int     # right color AND right position ("black pegs")
    partial_matches: int   # right color, wrong position   ("white pegs")
    def is_solved(self, code_length):
        """True when every position is an exact match (the code is cracked)."""
        return self.exact_matches == code_length
    def __str__(self):
        pegs = '● ' * self.exact_matches + '○ ' * self.partial_matches
        detail = '({} exact, {} partial)'.format(self.exact_matches, self.partial_matches)
        rendered = pegs.strip() if pegs.strip() else '—'
        return '{} {}'.format(rendered, detail)
def evaluate_guess(secret, guess):
    """
    Compare `guess` to `secret` (both lists of color symbols of equal length).
    Returns a Feedback with the number of exact and partial matches.
    Partial matches never double-count a color already used for an exact
    match, following standard Mastermind scoring rules.
    """
    if len(secret) != len(guess):
        raise ValueError('Secret and guess must have the same length.')
    exact = 0
    secret_left = []
    guess_left = []
    for secret_color, guess_color in zip(secret, guess):
        if secret_color == guess_color:
            exact += 1
        else:
            secret_left.append(secret_color)
            guess_left.append(guess_color)
    secret_counts = Counter(secret_left)
    guess_counts = Counter(guess_left)
    partial = sum(
        min(count, secret_counts[color])
        for color, count in guess_counts.items()
    )
    return Feedback(exact_matches=exact, partial_matches=partial)