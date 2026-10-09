"""Mastermind game logic: secret generation, guess parsing, scoring, game loop."""
import random

COLORS = ("R", "G", "B", "Y", "O", "P")
COLOR_NAMES = {
    "R": "Red", "G": "Green", "B": "Blue",
    "Y": "Yellow", "O": "Orange", "P": "Purple",
}
CODE_LENGTH = 4
MAX_ATTEMPTS = 10


class InputClosed(Exception):
    """Raised when stdin is exhausted (EOF) or interrupted."""


def read_line(prompt=""):
    """Read a line from stdin, converting EOF/interrupt into InputClosed."""
    try:
        return input(prompt)
    except EOFError:
        raise InputClosed() from None
    except KeyboardInterrupt:
        raise InputClosed() from None


def generate_secret(length=CODE_LENGTH, colors=COLORS):
    """Random hidden code; repeats allowed."""
    return [random.choice(colors) for _ in range(length)]


def parse_guess(text, length=CODE_LENGTH, colors=COLORS):
    """Return a list of color letters, or None if the guess is invalid."""
    tokens = text.upper().replace(",", " ").split()
    if len(tokens) != length:
        return None
    guess = []
    for token in tokens:
        if len(token) == 1 and token in colors:
            guess.append(token)
        else:
            return None
    return guess


def score_guess(secret, guess):
    """Return (exact, partial): exact = right color & position,
    partial = right color, wrong position (peg-count aware)."""
    exact = sum(1 for s, g in zip(secret, guess) if s == g)
    secret_left, guess_left = {}, {}
    for s, g in zip(secret, guess):
        if s != g:
            secret_left[s] = secret_left.get(s, 0) + 1
            guess_left[g] = guess_left.get(g, 0) + 1
    partial = sum(min(secret_left[c], guess_left.get(c, 0)) for c in secret_left)
    return exact, partial


class MastermindGame:
    def __init__(self, attempts=MAX_ATTEMPTS, length=CODE_LENGTH, secret=None):
        self.length = length
        self.attempts = attempts
        self.secret = secret if secret is not None else generate_secret(length)
        self.history = []

    def play(self):
        print(f"\nGuess the hidden {self.length}-color code (repeats allowed).")
        print("Colors:", " ".join(f"{c}({COLOR_NAMES[c]})" for c in COLORS))
        print(f"You have {self.attempts} tries. Enter letters separated by spaces, e.g. 'R G B Y'.\n")
        turn = 0
        try:
            while turn < self.attempts:
                raw = read_line(f"Attempt {turn + 1}/{self.attempts} - your guess: ").strip()
                guess = parse_guess(raw, self.length)
                if guess is None:
                    print(f"Invalid guess. Enter {self.length} letters from {' '.join(COLORS)}.\n")
                    continue
                turn += 1
                exact, partial = score_guess(self.secret, guess)
                self.history.append((turn, guess, exact, partial))
                print(f"You guessed : {' '.join(guess)}")
                print(f"Feedback    : exact (color+position) = {exact} | partial (color only) = {partial}\n")
                if exact == self.length:
                    print(f"YOU WIN! Cracked the code in {turn} attempt(s): {' '.join(self.secret)}")
                    return True
        except InputClosed:
            print(f"\nInput stream closed. The secret code was: {' '.join(self.secret)}")
            raise
        print(f"GAME OVER - you lost. The secret code was: {' '.join(self.secret)}")
        return False