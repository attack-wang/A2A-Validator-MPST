#!/usr/bin/env python3
"""Mastermind: crack the hidden color code within the allowed number of tries."""

import random
import sys
from collections import Counter

COLORS = ["R", "G", "B", "Y", "O", "P"]
COLOR_NAMES = {"R": "Red", "G": "Green", "B": "Blue",
               "Y": "Yellow", "O": "Orange", "P": "Purple"}
CODE_LENGTH = 4
MAX_TRIES = 10


def generate_code(colors, length):
    """Secret code: `length` colors picked with repetition allowed."""
    return [random.choice(colors) for _ in range(length)]


def parse_guess(raw, colors, length):
    """Return list of color letters, or None if the guess is invalid."""
    tokens = raw.strip().upper().replace(",", " ").split()
    if len(tokens) == 1 and len(tokens[0]) == length and all(ch in colors for ch in tokens[0]):
        return list(tokens[0])
    if len(tokens) != length or not all(t in colors for t in tokens):
        return None
    return tokens


def score_guess(code, guess):
    """Return (exact, partial): exact = right color+spot, partial = right color, wrong spot."""
    exact = sum(1 for c, g in zip(code, guess) if c == g)
    code_counts, guess_counts = Counter(code), Counter(guess)
    color_matches = sum(min(code_counts[c], guess_counts[c]) for c in code_counts)
    return exact, color_matches - exact


def render_feedback(exact, partial):
    return "Exact: {}  Partial: {}  [{}{}]".format(
        exact, partial, "X" * exact, "O" * partial)


def print_history(history):
    for n, guess, exact, partial in history:
        print("  #{}: {} -> {}".format(n, " ".join(guess), render_feedback(exact, partial)))


def main():
    print("=" * 46)
    print("MASTERMIND")
    print("=" * 46)
    print("Guess the hidden code of {} colors.".format(CODE_LENGTH))
    print("Colors: " + ", ".join("{}={}".format(c, COLOR_NAMES[c]) for c in COLORS))
    print("Enter {} letters, e.g. 'RGBY' or 'R G B Y'.".format(CODE_LENGTH))
    print("X = exact (right color, right spot); O = partial (right color, wrong spot).")
    print("You have {} tries. Type 'quit' to give up.\n".format(MAX_TRIES))

    code = generate_code(COLORS, CODE_LENGTH)
    history = []

    for attempt in range(1, MAX_TRIES + 1):
        while True:
            raw = input("Try {}/{} > ".format(attempt, MAX_TRIES))
            if raw.strip().lower() in ("quit", "q", "exit"):
                print("You gave up. The code was: " + " ".join(code))
                return
            guess = parse_guess(raw, COLORS, CODE_LENGTH)
            if guess is None:
                print("Invalid guess. Enter exactly {} of: {}".format(
                    CODE_LENGTH, "".join(COLORS)))
                continue
            break

        exact, partial = score_guess(code, guess)
        history.append((attempt, guess, exact, partial))
        print_history(history)
        print()

        if exact == CODE_LENGTH:
            print("YOU WIN! Cracked the code {} in {} {}.".format(
                " ".join(code), attempt,
                "try" if attempt == 1 else "tries"))
            return

    print("GAME OVER - out of tries. The code was: " + " ".join(code))


if __name__ == "__main__":
    try:
        main()
    except (KeyboardInterrupt, EOFError):
        print("\nBye!")
        sys.exit(0)