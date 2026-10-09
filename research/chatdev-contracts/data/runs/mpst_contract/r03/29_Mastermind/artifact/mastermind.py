"""Core logic for the Mastermind code-breaking game."""

import random
from collections import Counter

DEFAULT_COLORS = ["R", "G", "B", "Y", "O", "P"]
CODE_LENGTH = 4
MAX_TRIES = 10


def generate_secret(colors=None, length=CODE_LENGTH, rng=None):
    """Return a random hidden code as a list of color letters.

    Colors may repeat. Pass a custom `rng` (with .choice) for testing.
    """
    colors = DEFAULT_COLORS if colors is None else colors
    rng = random if rng is None else rng
    return [rng.choice(colors) for _ in range(length)]


def evaluate_guess(secret, guess):
    """Return (exact, partial) match counts for a guess against the secret.

    exact   = right color in the right position
    partial = right color in the wrong position (never double-counted;
              each color in the secret is matched at most once)
    """
    exact = sum(1 for s, g in zip(secret, guess) if s == g)
    secret_counts = Counter(secret)
    guess_counts = Counter(guess)
    common = sum(min(secret_counts[c], guess_counts[c]) for c in secret_counts)
    return exact, common - exact


def validate_guess(raw, colors=None, length=CODE_LENGTH):
    """Validate raw user input.

    Returns (guess, error): on success (cleaned_guess, None);
    on failure (None, message). Exactly one element is None.
    """
    colors = DEFAULT_COLORS if colors is None else colors
    guess = raw.strip().upper().replace(" ", "")
    if len(guess) != length:
        return None, f"Guess must be exactly {length} characters."
    for ch in guess:
        if ch not in colors:
            return None, f"Invalid color '{ch}'. Valid colors: {' '.join(colors)}"
    return guess, None