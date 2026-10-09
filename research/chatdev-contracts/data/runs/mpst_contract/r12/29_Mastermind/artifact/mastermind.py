"""Core logic for the classic Mastermind code-breaking game."""
import random
from collections import Counter

COLORS = "RGBYOP"
CODE_LENGTH = 4
MAX_TRIES = 10


def generate_code(length=CODE_LENGTH, colors=COLORS):
    """Return a random hidden code as a list of color letters (repeats allowed)."""
    return [random.choice(colors) for _ in range(length)]


def evaluate_guess(code, guess):
    """Return (exact, partial) peg counts for a guess against the hidden code.

    exact   = right color in the right position
    partial = right color in the wrong position (counted via multiset overlap)
    """
    exact = sum(c == g for c, g in zip(code, guess))
    common = sum((Counter(code) & Counter(guess)).values())
    return exact, common - exact


def parse_guess(text, length=CODE_LENGTH, colors=COLORS):
    """Validate raw input; return a list of color letters, or None if invalid."""
    text = text.strip().upper().replace(" ", "").replace(",", "")
    if len(text) == length and all(ch in colors for ch in text):
        return list(text)
    return None