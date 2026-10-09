'''
feedback.py
Scoring logic for Mastermind guesses.
Turns a guess into structured feedback that distinguishes exact
matches (right color in the right position - the classic "black
pegs") from partial matches (right color in the wrong position - the
classic "white pegs"). Duplicate colors are handled correctly by
matching remaining colors by multiplicity.
'''
from collections import Counter
from dataclasses import dataclass
@dataclass(frozen=True)
class Feedback:
    """Immutable outcome of scoring one guess against the secret code."""
    exact: int    # right color in the right position ("black pegs")
    partial: int  # right color in the wrong position ("white pegs")
    def is_perfect(self, code_length):
        """True when every position of the guess is an exact match."""
        return self.exact == code_length and self.partial == 0
    def as_symbols(self, exact_symbol, partial_symbol, empty_symbol, code_length):
        """Render the feedback as a peg-style string such as '●●○○·'."""
        slots = (
            [exact_symbol] * self.exact
            + [partial_symbol] * self.partial
            + [empty_symbol] * (code_length - self.exact - self.partial)
        )
        return "".join(slots)
    def __str__(self):
        return f"{self.exact} exact, {self.partial} partial"
def compute_feedback(secret, guess):
    """
    Score `guess` against `secret` and return a Feedback object.
    Exact matches are counted position by position first. The colors
    remaining on each side (i.e. colors not consumed by an exact match)
    are then paired up by multiplicity, and each such pair is one
    partial match. This is the standard Mastermind scoring rule and it
    copes correctly with duplicated colors.
    """
    if len(secret) != len(guess):
        raise ValueError(
            f"Secret (length {len(secret)}) and guess (length {len(guess)}) "
            f"must have the same length."
        )
    # Pass 1: exact matches (right color in the right position).
    exact = sum(1 for s, g in zip(secret, guess) if s == g)
    # Pass 2: total color matches by multiplicity; subtracting the exact
    # matches leaves the partial matches (right color, wrong position).
    secret_counts = Counter(secret)
    guess_counts = Counter(guess)
    total_color_matches = sum(
        min(secret_counts[color], guess_counts[color]) for color in secret_counts
    )
    partial = total_color_matches - exact
    return Feedback(exact=exact, partial=partial)