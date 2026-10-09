"""Mastermind: break the hidden color code!

Run: python main.py
"""

import sys

from mastermind import (
    CODE_LENGTH,
    DEFAULT_COLORS,
    MAX_TRIES,
    evaluate_guess,
    generate_secret,
    validate_guess,
)


def safe_input(prompt):
    """Read input, exiting gracefully if stdin is closed (EOF or Ctrl-C)."""
    try:
        return input(prompt)
    except (EOFError, KeyboardInterrupt):
        print("\nInput stream closed. Exiting Mastermind. Goodbye!")
        sys.exit(0)


def play():
    print("=" * 44)
    print("              MASTERMIND")
    print("=" * 44)
    print(f"Guess the hidden {CODE_LENGTH}-color code.")
    print(f"Colors: {' '.join(DEFAULT_COLORS)}")
    print(f"You have {MAX_TRIES} tries.")
    print("Feedback pegs: X = exact (right color, right spot),")
    print("               O = partial (right color, wrong spot),")
    print("               - = color not in code (peg order is random).\n")

    secret = generate_secret()

    for attempt in range(1, MAX_TRIES + 1):
        while True:
            raw = safe_input(f"Try {attempt}/{MAX_TRIES} - enter your guess (e.g. RGBY): ")
            guess, error = validate_guess(raw)
            if error is None:
                break
            print(f"  Invalid input: {error}")

        exact, partial = evaluate_guess(secret, guess)
        pegs = ["X"] * exact + ["O"] * partial + ["-"] * (CODE_LENGTH - exact - partial)
        print(f"  Guess: {' '.join(guess)}  ->  Pegs: {' '.join(pegs)}")
        print(f"  (Exact: {exact}, Partial: {partial})\n")

        if exact == CODE_LENGTH:
            print(f"*** YOU WIN! You cracked the code {' '.join(secret)} "
                  f"in {attempt} tries. ***")
            return

    print(f"--- GAME OVER. You lose! The secret code was {' '.join(secret)}. ---")


def main():
    while True:
        play()
        again = safe_input("Play again? (y/n): ").strip().lower()
        if again != "y":
            print("Thanks for playing Mastermind. Goodbye!")
            break


if __name__ == "__main__":
    main()