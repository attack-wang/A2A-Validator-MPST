"""Mastermind: crack the hidden color code!"""

import random
import sys

COLORS = ["R", "G", "B", "Y", "O", "P"]  # Red, Green, Blue, Yellow, Orange, Purple
CODE_LENGTH = 4
MAX_ATTEMPTS = 10

COLOR_NAMES = {
    "R": "Red", "G": "Green", "B": "Blue",
    "Y": "Yellow", "O": "Orange", "P": "Purple",
}


def generate_secret():
    """Computer picks a hidden code; repeats allowed."""
    return [random.choice(COLORS) for _ in range(CODE_LENGTH)]


def evaluate_guess(secret, guess):
    """Return (exact, partial).

    exact   = right color in the right position
    partial = right color in the wrong position (no double counting)
    """
    exact = sum(s == g for s, g in zip(secret, guess))
    secret_counts = {}
    guess_counts = {}
    for s, g in zip(secret, guess):
        if s != g:
            secret_counts[s] = secret_counts.get(s, 0) + 1
            guess_counts[g] = guess_counts.get(g, 0) + 1
    partial = sum(min(n, guess_counts.get(c, 0)) for c, n in secret_counts.items())
    return exact, partial


def parse_guess(raw):
    """Validate raw input; return list of color letters or None."""
    raw = raw.strip().upper().replace(" ", "")
    if len(raw) != CODE_LENGTH or any(ch not in COLORS for ch in raw):
        return None
    return list(raw)


def play_round():
    secret = generate_secret()
    print("\nNew game! I've chosen a code of {} colors from: {}".format(
        CODE_LENGTH, ", ".join("{} ({})".format(c, COLOR_NAMES[c]) for c in COLORS)))
    print("Repeats are allowed. You have {} attempts. Good luck!\n".format(MAX_ATTEMPTS))

    for attempt in range(1, MAX_ATTEMPTS + 1):
        raw = input("Attempt {}/{} - enter {} colors (e.g. RGBY): ".format(
            attempt, MAX_ATTEMPTS, CODE_LENGTH))
        guess = parse_guess(raw)
        if guess is None:
            print("Invalid guess. Use exactly {} letters from: {}\n".format(
                CODE_LENGTH, ", ".join(COLORS)))
            continue
        exact, partial = evaluate_guess(secret, guess)
        if exact == CODE_LENGTH:
            print("\n*** You cracked it! The code was {}. ***".format("".join(secret)))
            print("Solved in {} attempt(s). You WIN!\n".format(attempt))
            return True
        print("Feedback -> Exact matches: {} | Partial matches: {}\n".format(exact, partial))

    print("Out of attempts! The secret code was {}. You LOSE.\n".format("".join(secret)))
    return False


def main():
    print("=" * 50)
    print("       WELCOME TO MASTERMIND (Python Edition)")
    print("=" * 50)
    wins = losses = 0
    while True:
        if play_round():
            wins += 1
        else:
            losses += 1
        print("Score -> Wins: {} | Losses: {}".format(wins, losses))
        again = input("Play again? (y/n): ").strip().lower()
        if again not in ("y", "yes"):
            print("Thanks for playing Mastermind. Goodbye!")
            break


if __name__ == "__main__":
    try:
        main()
    except (KeyboardInterrupt, EOFError):
        print("\nGame aborted. Goodbye!")
        sys.exit(0)