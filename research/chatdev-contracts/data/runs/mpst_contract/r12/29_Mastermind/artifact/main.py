"""CLI entry point for the classic Mastermind code-breaking game."""
from mastermind import (
    COLORS,
    CODE_LENGTH,
    MAX_TRIES,
    generate_code,
    evaluate_guess,
    parse_guess,
)


def read_guess(attempt):
    """Prompt until the player enters a valid guess; return it as a list of letters."""
    while True:
        raw = input(f"Try {attempt}/{MAX_TRIES} - enter {CODE_LENGTH} colors (e.g. RGBY): ")
        guess = parse_guess(raw)
        if guess:
            return guess
        print(f"  Invalid input. Use exactly {CODE_LENGTH} letters from {COLORS}.")


def play():
    code = generate_code()
    print("=" * 44)
    print("MASTERMIND")
    print("=" * 44)
    print(f"Colors: {' '.join(COLORS)}  (repeats allowed)")
    print(f"Crack the hidden {CODE_LENGTH}-color code within {MAX_TRIES} tries.")
    print("Feedback: Exact = right color & position,")
    print("          Partial = right color, wrong position.")
    print("-" * 44)
    for attempt in range(1, MAX_TRIES + 1):
        guess = read_guess(attempt)
        exact, partial = evaluate_guess(code, guess)
        print(f"  Guess: {' '.join(guess)} -> Exact: {exact} | Partial: {partial}")
        if exact == CODE_LENGTH:
            print(f"\n*** YOU WIN! Cracked the code in {attempt} tries. ***")
            return
    print(f"\n*** YOU LOSE! The hidden code was: {' '.join(code)} ***")


if __name__ == "__main__":
    play()