import datetime
import random
import sys

from colors import BOLD, GREEN, GREY, RESET, YELLOW
from words import ANSWERS, VALID_GUESSES

MAX_TURNS = 6
WORD_LEN = 5


def daily_word():
    """Deterministic word of the day based on the calendar date."""
    return ANSWERS[datetime.date.today().toordinal() % len(ANSWERS)]


def feedback(guess, answer):
    """Return per-position colors: green (right spot), yellow (wrong spot), grey (absent)."""
    result = [GREY] * WORD_LEN
    remaining = {}
    for i, ch in enumerate(answer):
        if guess[i] == ch:
            result[i] = GREEN
        else:
            remaining[ch] = remaining.get(ch, 0) + 1
    for i, ch in enumerate(guess):
        if result[i] != GREEN and remaining.get(ch, 0) > 0:
            result[i] = YELLOW
            remaining[ch] -= 1
    return result


def render(guess, result):
    return " ".join(f"{color}{BOLD}{ch.upper()}{RESET}" for ch, color in zip(guess, result))


def read_guess(turn):
    """Prompt until a valid 5-letter dictionary word is entered; invalid input costs no turn."""
    while True:
        try:
            raw = input(f"Turn {turn}/{MAX_TURNS} - Enter a 5-letter word: ").strip().lower()
        except EOFError:
            print("\nInput stream closed. Goodbye.")
            sys.exit(0)
        except KeyboardInterrupt:
            print("\nInterrupted. Goodbye.")
            sys.exit(0)
        if len(raw) != WORD_LEN:
            print(f"Invalid guess: must be exactly {WORD_LEN} letters.")
        elif not raw.isalpha():
            print("Invalid guess: letters only.")
        elif raw not in VALID_GUESSES:
            print("Invalid guess: not in the word list.")
        else:
            return raw


def play(random_mode=False):
    answer = random.choice(ANSWERS) if random_mode else daily_word()
    print("=== ChatDev Terminal Wordle ===")
    print("Guess the 5-letter word.")
    print("Green = correct letter, correct spot | Yellow = correct letter, wrong spot | Grey = letter not in word.")
    print(f"You have {MAX_TURNS} attempts." + ("" if random_mode else " A new word is chosen each day."))
    print()
    board = []
    for turn in range(1, MAX_TURNS + 1):
        guess = read_guess(turn)
        board.append(render(guess, feedback(guess, answer)))
        print("\n".join(board))
        print()
        if guess == answer:
            print(f"{GREEN}{BOLD}You win! You guessed it in {turn} {'try' if turn == 1 else 'tries'}.{RESET}")
            return
    print(f"{GREY}Out of attempts. The word was {BOLD}{answer.upper()}{RESET}.")