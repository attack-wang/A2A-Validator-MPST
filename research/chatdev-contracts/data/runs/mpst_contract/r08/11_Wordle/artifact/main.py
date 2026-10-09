import datetime
import os
import random
import sys

from words import WORDS

GREEN, YELLOW, GREY, RESET = "\033[92m", "\033[93m", "\033[90m", "\033[0m"
BOLD = "\033[1m"
MAX_TURNS = 6
WORD_LEN = 5


def daily_word():
    today = datetime.date.today()
    rng = random.Random(today.toordinal())
    return rng.choice(WORDS)


def feedback(guess, answer):
    result = [GREY] * WORD_LEN
    counts = {}
    for ch in answer:
        counts[ch] = counts.get(ch, 0) + 1
    for i, ch in enumerate(guess):
        if ch == answer[i]:
            result[i] = GREEN
            counts[ch] -= 1
    for i, ch in enumerate(guess):
        if result[i] == GREY and counts.get(ch, 0) > 0:
            result[i] = YELLOW
            counts[ch] -= 1
    return result


def render(guess, colors):
    return " ".join(f"{c}{ch}{RESET}" for ch, c in zip(guess, colors))


def read_guess():
    try:
        return input("Enter guess: ")
    except (EOFError, KeyboardInterrupt):
        print("\nInput closed - goodbye.")
        sys.exit(0)


def get_guess(valid):
    while True:
        guess = read_guess().strip().lower()
        if len(guess) != WORD_LEN:
            print(f"Invalid guess: must be exactly {WORD_LEN} letters.")
        elif not guess.isalpha():
            print("Invalid guess: letters only.")
        elif guess not in valid:
            print("Invalid guess: not in word list.")
        else:
            return guess


def main():
    if os.name == "nt":
        os.system("")  # enable ANSI escape processing on Windows terminals
    answer = daily_word()
    valid = set(WORDS)
    print(BOLD + "WORDLE" + RESET)
    print(f"Daily word for {datetime.date.today().isoformat()} - guess the 5-letter word in 6 tries.")
    print("Green = right letter, right spot | Yellow = right letter, wrong spot | Grey = not in word\n")
    for turn in range(1, MAX_TURNS + 1):
        print(f"Turn {turn}/{MAX_TURNS}")
        guess = get_guess(valid)
        colors = feedback(guess, answer)
        print(render(guess, colors) + "\n")
        if guess == answer:
            print(f"{GREEN}{BOLD}You win! You guessed it in {turn} {'try' if turn == 1 else 'tries'}.{RESET}")
            return
    print(f"Out of turns. The word was: {BOLD}{answer.upper()}{RESET}")


if __name__ == "__main__":
    main()