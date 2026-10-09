#!/usr/bin/env python3
"""Mastermind: crack the hidden color code within the allowed number of tries."""

import random
from collections import Counter

COLORS = ["R", "G", "B", "Y", "O", "P"]
COLOR_NAMES = {"R": "Red", "G": "Green", "B": "Blue",
               "Y": "Yellow", "O": "Orange", "P": "Purple"}
CODE_LENGTH = 4
MAX_TRIES = 10


def generate_code():
    """Computer picks a hidden sequence; duplicates are allowed."""
    return [random.choice(COLORS) for _ in range(CODE_LENGTH)]


def parse_guess(raw):
    """Validate input; return list of color letters or None if invalid."""
    guess = raw.strip().upper().replace(" ", "")
    if len(guess) != CODE_LENGTH or any(c not in COLORS for c in guess):
        return None
    return list(guess)


def score_guess(code, guess):
    """Return (exact, partial): exact = right color+position, partial = right color wrong position."""
    exact = sum(1 for c, g in zip(code, guess) if c == g)
    code_counts = Counter(code)
    guess_counts = Counter(guess)
    total_color_matches = sum(min(code_counts[c], guess_counts[c]) for c in code_counts)
    partial = total_color_matches - exact
    return exact, partial


def main():
    print("=" * 46)
    print("Welcome to MASTERMIND!")
    print("=" * 46)
    print(f"I have hidden a code of {CODE_LENGTH} colors (duplicates possible).")
    print("Available colors: " + ", ".join(f"{c} ({COLOR_NAMES[c]})" for c in COLORS))
    print(f"You have {MAX_TRIES} tries to crack it.")
    print("Feedback legend: X = exact match (right color, right spot)")
    print("                 O = partial match (right color, wrong spot)")

    secret = generate_code()

    for attempt in range(1, MAX_TRIES + 1):
        while True:
            raw = input(f"\nTry {attempt}/{MAX_TRIES} - enter {CODE_LENGTH} colors (e.g. RGBY): ")
            guess = parse_guess(raw)
            if guess is not None:
                break
            print(f"Invalid guess. Use exactly {CODE_LENGTH} letters from: {''.join(COLORS)}")

        exact, partial = score_guess(secret, guess)
        feedback = "X " * exact + "O " * partial
        print(f"Guess: {' '.join(guess)}  ->  Feedback: {feedback.strip() or 'none'}")

        if exact == CODE_LENGTH:
            print(f"\n*** YOU WIN! You cracked the code {''.join(secret)} in {attempt} tries! ***")
            return

    print(f"\n--- GAME OVER. You lose! The secret code was {''.join(secret)}. ---")


if __name__ == "__main__":
    main()