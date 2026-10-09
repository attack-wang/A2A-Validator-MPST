import random
import sys
from collections import Counter

CODE_LENGTH = 4
NUM_COLORS = 6
MAX_TRIES = 10
COLOR_NAMES = {1: "Red", 2: "Orange", 3: "Yellow", 4: "Green", 5: "Blue", 6: "Purple"}


def generate_code():
    return [random.randint(1, NUM_COLORS) for _ in range(CODE_LENGTH)]


def parse_guess(raw):
    raw = raw.strip().replace(" ", "")
    if len(raw) != CODE_LENGTH or not raw.isdigit():
        return None
    guess = [int(ch) for ch in raw]
    if any(n < 1 or n > NUM_COLORS for n in guess):
        return None
    return guess


def evaluate(guess, secret):
    exact = sum(1 for g, s in zip(guess, secret) if g == s)
    common = sum((Counter(guess) & Counter(secret)).values())
    return exact, common - exact


def format_pegs(exact, partial):
    pegs = ["B"] * exact + ["W"] * partial + ["-"] * (CODE_LENGTH - exact - partial)
    return " ".join(pegs)


def code_to_text(code):
    names = ", ".join(COLOR_NAMES[n] for n in code)
    return "".join(map(str, code)) + " (" + names + ")"


def prompt(message):
    try:
        return input(message)
    except (EOFError, KeyboardInterrupt):
        print("\nInput stream closed. Thanks for playing Mastermind. Goodbye!")
        sys.exit(0)


def play_round():
    secret = generate_code()
    for attempt in range(1, MAX_TRIES + 1):
        while True:
            raw = prompt(f"Guess {attempt}/{MAX_TRIES} ({CODE_LENGTH} digits, 1-{NUM_COLORS}): ")
            guess = parse_guess(raw)
            if guess is not None:
                break
            print(f"  Invalid input: enter exactly {CODE_LENGTH} digits, each between 1 and {NUM_COLORS}.")
        exact, partial = evaluate(guess, secret)
        print(f"  {''.join(map(str, guess))} -> {format_pegs(exact, partial)}")
        if exact == CODE_LENGTH:
            print(f"  All pegs exact in {attempt} tries - you cracked the code {code_to_text(secret)}. YOU WIN!")
            return True
    print(f"  Out of tries. The secret code was {code_to_text(secret)}. YOU LOSE.")
    return False


def main():
    print("=== MASTERMIND ===")
    print("Colors: " + ", ".join(f"{n}={name}" for n, name in COLOR_NAMES.items()))
    print(f"Guess the hidden {CODE_LENGTH}-color code within {MAX_TRIES} tries.")
    print("Feedback pegs: B = right color & right position, W = right color & wrong position, - = no match.")
    while True:
        play_round()
        if prompt("Play again? (y/n): ").strip().lower() != "y":
            print("Thanks for playing Mastermind. Goodbye!")
            break


if __name__ == "__main__":
    main()