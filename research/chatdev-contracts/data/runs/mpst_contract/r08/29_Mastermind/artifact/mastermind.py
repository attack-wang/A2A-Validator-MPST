"""Core rules for the Mastermind code-breaking game."""

import random
from collections import Counter

COLORS = ["R", "G", "B", "Y", "O", "P"]
COLOR_NAMES = {"R": "Red", "G": "Green", "B": "Blue",
               "Y": "Yellow", "O": "Orange", "P": "Purple"}
CODE_LENGTH = 4
MAX_TRIES = 10


def generate_secret_code(length=CODE_LENGTH, colors=COLORS):
    """Return a random hidden code; duplicate colors are allowed."""
    return [random.choice(colors) for _ in range(length)]


def parse_guess(raw, length=CODE_LENGTH, colors=COLORS):
    """Validate raw input and return a guess list, or None if invalid."""
    tokens = raw.upper().replace(",", " ").split()
    if len(tokens) != length:
        return None
    guess = []
    for token in tokens:
        if len(token) == 1 and token in colors:
            guess.append(token)
        else:
            return None
    return guess


def score_guess(guess, secret):
    """Return (exact, partial) peg counts for guess vs secret.

    exact   = positions where guess and secret match
    partial = colors present in both but placed in the wrong position
    """
    exact = sum(1 for g, s in zip(guess, secret) if g == s)
    overlap = sum((Counter(secret) & Counter(guess)).values())
    partial = overlap - exact
    return exact, partial