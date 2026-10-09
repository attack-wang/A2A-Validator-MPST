'''
feedback.py
Mastermind feedback (peg scoring) calculation.
Implements the classic scoring rules in a duplicate-safe way:
  * an EXACT match (black peg)  = right color in the right position;
  * a PARTIAL match (white peg) = right color in the wrong position.
Partial matches are computed by intersecting color histograms, which
correctly handles codes containing repeated colors.
'''
from collections import Counter
# Characters used to render feedback pegs (ASCII-safe for any terminal).
EXACT_PEG = "*"
PARTIAL_PEG = "o"
EMPTY_PEG = "-"
def calculate_feedback(guess, secret):
    """Score a guess against the secret; returns (exact, partial) peg counts."""
    if len(guess) != len(secret):
        raise ValueError("Guess and secret must have the same length.")
    exact = sum(1 for g, s in zip(guess, secret) if g == s)
    guess_counts = Counter(guess)
    secret_counts = Counter(secret)
    total_color_matches = sum(
        min(count, secret_counts.get(color, 0))
        for color, count in guess_counts.items()
    )
    partial = total_color_matches - exact
    return exact, partial
def feedback_pegs(exact, partial, code_length):
    """Render feedback as a fixed-width peg string, e.g. '* o - -'."""
    pegs = (
        [EXACT_PEG] * exact
        + [PARTIAL_PEG] * partial
        + [EMPTY_PEG] * max(0, code_length - exact - partial)
    )
    return " ".join(pegs)
def format_feedback(exact, partial, code_length):
    """Render pegs plus an explicit textual count, e.g. '* o - -  (1 exact, 1 partial)'."""
    pegs = feedback_pegs(exact, partial, code_length)
    return f"{pegs}  ({exact} exact, {partial} partial)"