'''
feedback.py
Scores a guess against the secret code using classic Mastermind rules.
Exact matches ("black pegs") are right color + right position; partial
matches ("white pegs") are right color + wrong position. The two-pass
algorithm below is the standard correct approach: colors consumed by
exact matches are removed first, so duplicates are never double-counted.
'''
from collections import Counter
from game_config import EXACT_SYMBOL, PARTIAL_SYMBOL, MISS_SYMBOL
class FeedbackResult:
    """Value object holding the peg counts for a single guess."""
    def __init__(self, exact, partial, code_length):
        self.exact = exact
        self.partial = partial
        self.code_length = code_length
    @property
    def is_win(self):
        """True when every position is an exact match."""
        return self.exact == self.code_length
    def pegs(self):
        """Render the feedback as a plain string of peg symbols."""
        return (EXACT_SYMBOL * self.exact
                + PARTIAL_SYMBOL * self.partial
                + MISS_SYMBOL * (self.code_length - self.exact - self.partial))
    def __str__(self):
        return f"{self.pegs()}  ({self.exact} exact, {self.partial} partial)"
class FeedbackCalculator:
    """Converts (guess, secret) pairs into FeedbackResult objects."""
    def __init__(self, code_length):
        self._code_length = code_length
    def calculate(self, guess, secret):
        """Score `guess` against `secret` and return a FeedbackResult."""
        exact = 0
        guess_leftover = []
        secret_leftover = []
        # Pass 1: exact matches; keep unmatched colors for pass 2.
        for guess_color, secret_color in zip(guess, secret):
            if guess_color == secret_color:
                exact += 1
            else:
                guess_leftover.append(guess_color)
                secret_leftover.append(secret_color)
        # Pass 2: partial matches via leftover color-count intersection.
        secret_counts = Counter(secret_leftover)
        partial = 0
        for color in guess_leftover:
            if secret_counts[color] > 0:
                partial += 1
                secret_counts[color] -= 1
        return FeedbackResult(exact, partial, self._code_length)