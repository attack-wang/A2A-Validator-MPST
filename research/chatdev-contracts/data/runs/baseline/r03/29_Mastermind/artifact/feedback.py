'''
feedback.py
Core Mastermind feedback logic. Converts a guess into the classic
black/white peg counts:
* exact_matches   -> right color in the right position   ("black pegs")
* partial_matches -> right color in the wrong position   ("white pegs")
The algorithm is duplicate-safe: it first counts positional hits, then
counts the multiset overlap of colors between guess and secret, and
subtracts the exact hits so a color is never double-counted.
'''
from collections import Counter
from dataclasses import dataclass
@dataclass(frozen=True)
class Feedback:
    """Immutable feedback result for a single guess."""
    exact_matches: int
    partial_matches: int
    code_length: int
    @property
    def is_win(self) -> bool:
        """True when every position of the guess matches the secret."""
        return self.exact_matches == self.code_length
    def __str__(self) -> str:
        return f"exact={self.exact_matches}, partial={self.partial_matches}"
def calculate_feedback(guess, secret) -> Feedback:
    """
    Compute (exact, partial) feedback for `guess` against `secret`.
    Both sequences must be same-length lists of comparable color tokens.
    """
    if len(guess) != len(secret):
        raise ValueError("Guess and secret must have the same length.")
    # 1) Exact matches: same color at the same position.
    exact = sum(1 for g, s in zip(guess, secret) if g == s)
    # 2) Total color overlap: for each color, how many copies appear in
    #    both sequences (multiset intersection), regardless of position.
    guess_counts = Counter(guess)
    secret_counts = Counter(secret)
    overlap = sum(min(count, secret_counts.get(color, 0))
                  for color, count in guess_counts.items())
    # 3) Partial matches are the overlap minus the exact hits, so a color
    #    matched in place is never counted again as a partial match.
    partial = overlap - exact
    return Feedback(exact_matches=exact, partial_matches=partial, code_length=len(secret))