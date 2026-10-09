"""Core logic for the classic Mastermind code-breaking game."""
import random
from collections import Counter

DEFAULT_PALETTE = ["R", "G", "B", "Y", "O", "P"]
COLOR_NAMES = {
    "R": "Red", "G": "Green", "B": "Blue",
    "Y": "Yellow", "O": "Orange", "P": "Purple",
}


class MastermindGame:
    """Hidden-code game: exact matches (peg X) vs partial matches (peg O)."""

    def __init__(self, code_length=4, max_tries=10, palette=None, rng=random):
        self.palette = list(palette) if palette else list(DEFAULT_PALETTE)
        self.code_length = code_length
        self.max_tries = max_tries
        self.rng = rng
        self.secret = [self.rng.choice(self.palette) for _ in range(code_length)]
        self.history = []

    def evaluate(self, guess):
        """Return (exact, partial).

        exact   = right color in the right position.
        partial = right color in the wrong position (counted per color surplus).
        """
        exact = sum(1 for g, s in zip(guess, self.secret) if g == s)
        guess_rest = Counter(g for g, s in zip(guess, self.secret) if g != s)
        secret_rest = Counter(s for g, s in zip(guess, self.secret) if g != s)
        partial = sum(min(guess_rest[c], secret_rest[c]) for c in guess_rest)
        return exact, partial

    def parse_guess(self, text):
        """Normalize raw input into a valid guess list, or None if invalid."""
        tokens = text.strip().upper().replace(",", " ").split()
        if not tokens:
            return None
        if len(tokens) == 1 and len(tokens[0]) == self.code_length:
            tokens = list(tokens[0])
        if len(tokens) != self.code_length:
            return None
        if all(t in self.palette for t in tokens):
            return tokens
        return None

    def play(self, input_fn=input, output_fn=print):
        """Run one full session; return True on win, False on loss."""
        output_fn("=" * 46)
        output_fn("MASTERMIND - Crack the hidden code!")
        output_fn("=" * 46)
        output_fn("Colors: " + ", ".join(
            f"{c} ({COLOR_NAMES.get(c, c)})" for c in self.palette))
        output_fn(f"Code length: {self.code_length} | Max tries: {self.max_tries}")
        output_fn("Feedback per guess:")
        output_fn("  X = exact match (right color, right position)")
        output_fn("  O = partial match (right color, wrong position)")
        output_fn("-" * 46)

        for attempt in range(1, self.max_tries + 1):
            guess = self._prompt_guess(attempt, input_fn, output_fn)
            exact, partial = self.evaluate(guess)
            self.history.append((list(guess), exact, partial))
            pegs = "X" * exact + "O" * partial + "." * (self.code_length - exact - partial)
            output_fn(f"  Guess {' '.join(guess)} | Feedback [{pegs}] "
                      f"| Exact: {exact} Partial: {partial}")
            if exact == self.code_length:
                output_fn("=" * 46)
                output_fn(f"YOU WIN! Cracked {' '.join(self.secret)} in {attempt} tries.")
                output_fn("=" * 46)
                return True

        output_fn("=" * 46)
        output_fn(f"YOU LOSE! The secret code was {' '.join(self.secret)}.")
        output_fn("=" * 46)
        return False

    def _prompt_guess(self, attempt, input_fn, output_fn):
        while True:
            try:
                raw = input_fn(
                    f"Try {attempt}/{self.max_tries} - enter {self.code_length} "
                    f"colors (e.g. RGBY): "
                )
            except (EOFError, KeyboardInterrupt):
                output_fn("\nGame aborted by player.")
                raise SystemExit(0)
            guess = self.parse_guess(raw)
            if guess is not None:
                return guess
            output_fn(f"  Invalid input. Use {self.code_length} colors from: "
                      f"{''.join(self.palette)}")