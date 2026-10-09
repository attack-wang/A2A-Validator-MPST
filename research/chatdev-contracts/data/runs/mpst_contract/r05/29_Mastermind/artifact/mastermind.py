"""Core logic for the classic Mastermind code-breaking game."""

import random

COLORS = ("R", "G", "B", "Y", "O", "P")
COLOR_NAMES = {
    "R": "Red", "G": "Green", "B": "Blue",
    "Y": "Yellow", "O": "Orange", "P": "Purple",
}
CODE_LENGTH = 4
MAX_TRIES = 10


class MastermindGame:
    """Holds the secret code, evaluates guesses, and tracks win/lose state."""

    def __init__(self, code_length=CODE_LENGTH, max_tries=MAX_TRIES,
                 colors=COLORS, rng=None):
        self.colors = tuple(colors)
        self.code_length = code_length
        self.max_tries = max_tries
        self.rng = rng if rng is not None else random
        self.secret = [self.rng.choice(self.colors) for _ in range(code_length)]
        self.tries_used = 0
        self.history = []
        self.won = False
        self.finished = False

    def is_valid_guess(self, text):
        """A valid guess is the right length and uses only available colors."""
        text = text.strip().upper()
        return len(text) == self.code_length and all(c in self.colors for c in text)

    def evaluate(self, guess):
        """Return (exact, partial) peg counts for a guess against the secret.

        exact   = right color in the right position (black pegs)
        partial = right color in the wrong position (white pegs)
        """
        exact = sum(1 for s, g in zip(self.secret, guess) if s == g)
        remaining_secret = {}
        remaining_guess = {}
        for s, g in zip(self.secret, guess):
            if s != g:
                remaining_secret[s] = remaining_secret.get(s, 0) + 1
                remaining_guess[g] = remaining_guess.get(g, 0) + 1
        partial = sum(min(n, remaining_guess.get(c, 0))
                      for c, n in remaining_secret.items())
        return exact, partial

    def submit_guess(self, guess):
        """Record a validated guess, update state, and return (exact, partial)."""
        if self.finished:
            raise RuntimeError("Game is already over.")
        self.tries_used += 1
        exact, partial = self.evaluate(guess)
        self.history.append((list(guess), exact, partial))
        if exact == self.code_length:
            self.won = True
            self.finished = True
        elif self.tries_used >= self.max_tries:
            self.finished = True
        return exact, partial