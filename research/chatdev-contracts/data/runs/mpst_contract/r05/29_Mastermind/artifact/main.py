"""CLI entry point for the classic Mastermind code-breaking game."""

import sys

from mastermind import MastermindGame, COLORS, COLOR_NAMES, CODE_LENGTH, MAX_TRIES


def format_feedback(exact, partial):
    return f"Black pegs (exact match): {exact} | White pegs (partial match): {partial}"


def read_line(prompt):
    """Read one line from stdin; return None on EOF or Ctrl-C."""
    try:
        return input(prompt)
    except EOFError:
        return None
    except KeyboardInterrupt:
        return None


def main():
    print("=" * 52)
    print("MASTERMIND")
    print("=" * 52)
    print(f"A hidden code of {CODE_LENGTH} colors has been generated.")
    print("Available colors: " + ", ".join(f"{c} ({COLOR_NAMES[c]})" for c in COLORS))
    print(f"You have {MAX_TRIES} tries to crack it.")
    print("Feedback after each guess:")
    print("  - Black peg: right color in the right position (exact match)")
    print("  - White peg: right color in the wrong position (partial match)")
    print(f"Enter your guess as {CODE_LENGTH} letters, e.g. RGBY.\n")

    game = MastermindGame()

    while not game.finished:
        raw = read_line(f"Try {game.tries_used + 1}/{game.max_tries} - Enter your guess: ")
        if raw is None:
            print("\nInput closed (EOF). Game ended early.")
            print(f"The hidden code was '{''.join(game.secret)}'.")
            return 0
        if not game.is_valid_guess(raw):
            print(f"Invalid guess. Use exactly {CODE_LENGTH} letters from {''.join(COLORS)}.\n")
            continue
        guess = list(raw.strip().upper())
        exact, partial = game.submit_guess(guess)
        print(f"Guess: {' '.join(guess)} -> {format_feedback(exact, partial)}\n")

    print("=" * 52)
    if game.won:
        print(f"YOU WIN! You cracked the code '{''.join(game.secret)}' "
              f"in {game.tries_used} of {game.max_tries} tries.")
    else:
        print(f"YOU LOSE. The hidden code was '{''.join(game.secret)}'.")
    print("=" * 52)
    return 0


if __name__ == "__main__":
    sys.exit(main())