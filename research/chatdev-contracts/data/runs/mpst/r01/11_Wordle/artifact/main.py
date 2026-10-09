'''
main.py
Entry point for the terminal-based Wordle game.
A daily 5-letter word is chosen deterministically from the system date.
The player has 6 attempts to guess it. After every guess the game prints
color-coded feedback in the Linux terminal:
    GREEN  -> correct letter in the correct position
    YELLOW -> correct letter in the wrong position
    GREY   -> letter not in the word at all
Guesses are validated (letters only, exactly 5 characters, must be a
known English word). Winning reveals a congratulation message; losing
(or quitting with 'q') reveals the hidden word.
Run with:  python3 main.py          (daily word)
           python3 main.py --random (random word for extra practice)
'''
import random
import sys
from collections import Counter
from datetime import date
from word_list import ANSWER_WORDS, VALID_WORDS
# ANSI escape codes for Linux terminal colors
GREEN = "\033[92m"    # correct letter, correct position
YELLOW = "\033[93m"   # correct letter, wrong position
GREY = "\033[90m"     # letter not in the word
RESET = "\033[0m"     # reset styling
MAX_ATTEMPTS = 6
WORD_LENGTH = 5
def get_feedback(guess, answer):
    """Return a list of color codes, one per letter of the guess.
    Two-pass algorithm handles duplicate letters correctly:
    first mark greens (consuming matched answer letters),
    then mark yellows using the remaining letter counts.
    """
    feedback = [GREY] * WORD_LENGTH
    answer_counts = Counter(answer)
    # First pass: greens
    for i, (g, a) in enumerate(zip(guess, answer)):
        if g == a:
            feedback[i] = GREEN
            answer_counts[g] -= 1
    # Second pass: yellows
    for i, (g, a) in enumerate(zip(guess, answer)):
        if feedback[i] == GREEN:
            continue
        if answer_counts.get(g, 0) > 0:
            feedback[i] = YELLOW
            answer_counts[g] -= 1
    return feedback
def get_daily_word():
    """Pick a deterministic 'word of the day' from today's date."""
    return ANSWER_WORDS[date.today().toordinal() % len(ANSWER_WORDS)].lower()
def get_random_word():
    """Pick a uniformly random word (used with the --random flag)."""
    return random.choice(ANSWER_WORDS).lower()
def render_guess(guess, feedback):
    """Return the colored terminal string for one guessed word."""
    return "".join(f"{color}{letter.upper()}{RESET}"
                   for letter, color in zip(guess, feedback))
def prompt_guess(attempt):
    """Read and validate one guess, re-prompting until it is acceptable.
    Valid guesses are alphabetic, exactly WORD_LENGTH characters long,
    and present in the VALID_WORDS dictionary. Typing 'q' quits.
    """
    while True:
        guess = input(f"Attempt {attempt}/{MAX_ATTEMPTS}: ").strip().lower()
        if guess == "q":
            return None
        if not guess.isalpha():
            print("Please enter letters only.")
        elif len(guess) != WORD_LENGTH:
            print(f"Your guess must be exactly {WORD_LENGTH} letters.")
        elif guess not in VALID_WORDS:
            print("Not a valid word. Try again.")
        else:
            return guess
def main():
    """Run the interactive Wordle game loop (6 attempts, validation, win/lose)."""
    answer = get_random_word() if "--random" in sys.argv else get_daily_word()
    print("Welcome to Wordle! Guess the 5-letter word.")
    print(f"You have {MAX_ATTEMPTS} attempts. (Type 'q' to quit)")
    try:
        for attempt in range(1, MAX_ATTEMPTS + 1):
            guess = prompt_guess(attempt)
            if guess is None:
                print(f"The word was: {answer.upper()}")
                return
            feedback = get_feedback(guess, answer)
            print(render_guess(guess, feedback))
            if guess == answer:
                print(f"Congratulations! You won in {attempt} attempt(s).")
                return
        print(f"You ran out of attempts. The word was: {answer.upper()}")
    except (KeyboardInterrupt, EOFError):
        print(f"\nGame interrupted. The word was: {answer.upper()}")
if __name__ == "__main__":
    main()