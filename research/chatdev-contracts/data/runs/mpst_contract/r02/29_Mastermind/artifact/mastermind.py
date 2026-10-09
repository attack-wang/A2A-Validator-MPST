"""Core logic for the classic Mastermind code-breaking game."""
import random

COLORS = ["R", "G", "B", "Y", "O", "P"]  # Red, Green, Blue, Yellow, Orange, Purple
CODE_LENGTH = 4
MAX_TRIES = 12


def generate_secret(colors=COLORS, length=CODE_LENGTH):
    """Computer picks a hidden code: colors may repeat."""
    return [random.choice(colors) for _ in range(length)]


def score_guess(secret, guess):
    """Return (exact, partial) pegs.

    exact   = right color in the right position
    partial = right color in the wrong position (each secret color counts once)
    """
    exact = sum(1 for s, g in zip(secret, guess) if s == g)
    secret_left = {}
    guess_left = {}
    for s, g in zip(secret, guess):
        if s != g:
            secret_left[s] = secret_left.get(s, 0) + 1
            guess_left[g] = guess_left.get(g, 0) + 1
    partial = sum(min(secret_left.get(c, 0), n) for c, n in guess_left.items())
    return exact, partial


def is_valid_guess(guess, colors=COLORS, length=CODE_LENGTH):
    """A valid guess has exactly `length` symbols, all from `colors`."""
    return len(guess) == length and all(c in colors for c in guess)