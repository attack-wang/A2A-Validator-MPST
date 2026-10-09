import datetime
import zlib

from words import ANSWER_LIST, VALID_GUESSES

GREEN = "\033[92m"
YELLOW = "\033[93m"
GREY = "\033[90m"
RESET = "\033[0m"
MAX_TURNS = 6
WORD_LEN = 5


def daily_word():
    """Deterministic word of the day: same word for everyone on a given date."""
    today = datetime.date.today().isoformat()
    idx = zlib.crc32(today.encode("utf-8")) % len(ANSWER_LIST)
    return ANSWER_LIST[idx]


def feedback(guess, answer):
    """Return per-position colors: green/yellow/grey, handling duplicates."""
    result = [GREY] * WORD_LEN
    remaining = {}
    for i, (g, a) in enumerate(zip(guess, answer)):
        if g == a:
            result[i] = GREEN
        else:
            remaining[a] = remaining.get(a, 0) + 1
    for i, g in enumerate(guess):
        if result[i] == GREY and remaining.get(g, 0) > 0:
            result[i] = YELLOW
            remaining[g] -= 1
    return result


def render(guess, colors):
    return " ".join(c + g.upper() + RESET for g, c in zip(guess, colors))


def get_guess(turn):
    while True:
        try:
            guess = input(f"Turn {turn}/{MAX_TURNS}> ").strip().lower()
        except (EOFError, KeyboardInterrupt):
            print("\nBye!")
            raise SystemExit(0)
        if len(guess) != WORD_LEN:
            print("Guess must be exactly 5 letters.")
        elif not guess.isalpha():
            print("Guess must contain letters only.")
        elif guess not in VALID_GUESSES:
            print("Not a recognized word. Try again.")
        else:
            return guess


def play():
    answer = daily_word()
    print("=== WORDLE (terminal) ===")
    print("Guess the 5-letter word in 6 tries.")
    print("Green = correct letter & position, Yellow = correct letter wrong position, Grey = letter not in word.")
    print(f"Today's date: {datetime.date.today().isoformat()}\n")
    for turn in range(1, MAX_TURNS + 1):
        guess = get_guess(turn)
        print(render(guess, feedback(guess, answer)) + "\n")
        if guess == answer:
            print(f"You win! Solved in {turn} {'try' if turn == 1 else 'tries'}.")
            return
    print(f"Out of turns. The word was: {answer.upper()}")