"""Mastermind: crack the hidden color code within the allowed tries."""

import sys

from mastermind import (CODE_LENGTH, COLORS, COLOR_NAMES, MAX_TRIES,
                        generate_secret_code, parse_guess, score_guess)


class InputClosed(Exception):
    """Raised when stdin reaches EOF or the player interrupts the session."""


def safe_input(prompt=""):
    """Read a line from the player; translate EOF/interrupt to InputClosed."""
    try:
        return input(prompt)
    except (EOFError, KeyboardInterrupt):
        raise InputClosed from None


def print_intro():
    print("=" * 50)
    print("MASTERMIND".center(50))
    print("=" * 50)
    print(f"A hidden code of {CODE_LENGTH} colors has been chosen from:")
    print("  " + "  ".join(f"{c} = {COLOR_NAMES[c]}" for c in COLORS))
    print("Duplicates are allowed. After each guess you get:")
    print("  Exact   = right color in the right position")
    print("  Partial = right color in the wrong position")
    print(f"You have {MAX_TRIES} tries. Enter guesses like: R G B Y")
    print("-" * 50)


def print_history(history):
    print("\nBoard so far:")
    for attempt, guess, exact, partial in history:
        print(f"  {attempt:>2}. {' '.join(guess)}   | "
              f"Exact: {exact}  Partial: {partial}")
    print("-" * 50)


def play_round():
    secret = generate_secret_code()
    history = []
    print_intro()
    attempt = 1
    while attempt <= MAX_TRIES:
        raw = safe_input(f"\nGuess {attempt}/{MAX_TRIES}: ").strip()
        guess = parse_guess(raw)
        if guess is None:
            print(f"  Invalid guess. Enter {CODE_LENGTH} colors from "
                  f"{' '.join(COLORS)}, e.g. 'R G B Y'. (Try not consumed.)")
            continue
        exact, partial = score_guess(guess, secret)
        history.append((attempt, guess, exact, partial))
        print(f"  -> {' '.join(guess)} | Exact: {exact}  Partial: {partial}")
        if exact == CODE_LENGTH:
            print_history(history)
            print(f"\n*** YOU WIN! You cracked the code "
                  f"{' '.join(secret)} in {attempt} try(ies). ***")
            return True
        attempt += 1
    print_history(history)
    print("\n--- GAME OVER. You are out of tries. You lose. ---")
    print(f"The hidden code was: {' '.join(secret)}")
    return False


def main():
    wins = 0
    rounds = 0
    try:
        while True:
            if play_round():
                wins += 1
            rounds += 1
            again = safe_input("\nPlay again? (y/n): ").strip().lower()
            if again != "y":
                break
    except InputClosed:
        print("\nInput stream closed. Ending the session early.")
    print(f"\nSession record: {wins} win(s) out of {rounds} round(s). "
          "Thanks for playing!")
    return 0


if __name__ == "__main__":
    sys.exit(main())