#!/usr/bin/env python3
"""Terminal Wordle."""
import random
import sys
from datetime import date

from words import WORDS

GREEN, YELLOW, GREY, RESET, BOLD = "\033[92m", "\033[93m", "\033[90m", "\033[0m", "\033[1m"

MAX_TURNS = 6
WORD_LEN = 5


def pick_daily_word():
    today = date.today().isoformat()
    rng = random.Random(today)
    return rng.choice(WORDS), today


def score_guess(guess, answer):
    """Return list of (letter, color) using standard Wordle rules."""
    result = [GREY] * WORD_LEN
    remaining = {}
    for i, ch in enumerate(answer):
        if guess[i] != ch:
            remaining[ch] = remaining.get(ch, 0) + 1
    for i, ch in enumerate(guess):
        if ch == answer[i]:
            result[i] = GREEN
        elif remaining.get(ch, 0) > 0:
            result[i] = YELLOW
            remaining[ch] -= 1
    return result


def render(guess, colors):
    return "".join(f"{c}{ch}{RESET}" for ch, c in zip(guess, colors))


def get_guess(attempt):
    while True:
        raw = input(f"Guess {attempt}/{MAX_TURNS}: ").strip().lower()
        if len(raw) != WORD_LEN:
            print(f"  Invalid: guess must be exactly {WORD_LEN} letters.")
        elif not raw.isalpha():
            print("  Invalid: letters only.")
        elif raw not in WORDS:
            print("  Invalid: not in word list.")
        else:
            return raw


def play():
    answer, day = pick_daily_word()
    print(BOLD + "WORDLE" + RESET + f"  -  daily puzzle for {day}")
    print(f"Guess the {WORD_LEN}-letter word in {MAX_TURNS} tries. "
          f"{GREEN}green{RESET}=right spot, {YELLOW}yellow{RESET}=wrong spot, {GREY}grey{RESET}=not in word.\n")
    for attempt in range(1, MAX_TURNS + 1):
        guess = get_guess(attempt)
        print("  " + render(guess, score_guess(guess, answer)) + "\n")
        if guess == answer:
            print(BOLD + f"You won in {attempt}/{MAX_TURNS}! The word was {answer.upper()}." + RESET)
            return
    print(BOLD + f"You lost. The word was {answer.upper()}." + RESET)


if __name__ == "__main__":
    try:
        play()
    except (KeyboardInterrupt, EOFError):
        print("\nGame aborted.")
        sys.exit(0)