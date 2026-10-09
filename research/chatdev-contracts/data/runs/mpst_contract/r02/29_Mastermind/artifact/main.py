"""Mastermind: crack the hidden color code before you run out of tries."""
from mastermind import (
    COLORS,
    CODE_LENGTH,
    MAX_TRIES,
    generate_secret,
    score_guess,
    is_valid_guess,
)


def parse_guess(raw):
    """Turn raw input like 'R G B Y', 'R,G,B,Y' or 'RGBY' into a list."""
    tokens = raw.replace(",", " ").split()
    if len(tokens) == 1 and len(tokens[0]) == CODE_LENGTH:
        return list(tokens[0])
    return tokens


def main():
    print("=" * 60)
    print("Welcome to MASTERMIND!")
    print(f"The computer has hidden a code of {CODE_LENGTH} colors.")
    print(f"Available colors: {' '.join(COLORS)}")
    print(f"You have {MAX_TRIES} tries. Example guess: R G B Y")
    print("Feedback: EXACT = right color & position, PARTIAL = right color, wrong position.")
    print("=" * 60)

    secret = generate_secret()
    won = False
    attempt = 0

    for attempt in range(1, MAX_TRIES + 1):
        while True:
            try:
                raw = input(f"\nAttempt {attempt}/{MAX_TRIES} - enter your guess: ")
            except (EOFError, KeyboardInterrupt):
                print("\nGame aborted.")
                return
            guess = parse_guess(raw.strip().upper())
            if is_valid_guess(guess):
                break
            print(f"Invalid guess. Enter exactly {CODE_LENGTH} colors from: {' '.join(COLORS)}")

        exact, partial = score_guess(secret, guess)
        print(f"Guess: {' '.join(guess)}")
        print(f"  Exact matches (correct color + position):   {exact}")
        print(f"  Partial matches (correct color, wrong pos): {partial}")

        if exact == CODE_LENGTH:
            won = True
            break

    if won:
        print(f"\n*** YOU WIN! You cracked the code {' '.join(secret)} in {attempt} tries! ***")
    else:
        print(f"\n--- GAME OVER. You lost! The secret code was {' '.join(secret)}. ---")


if __name__ == "__main__":
    main()