'''
main.py
Entry point for the terminal Wordle game...
'''
import argparse
import datetime
import sys
from game import WordleGame, MAX_ATTEMPTS, WORD_LENGTH
from word_manager import WordManager
from colors import set_color_enabled, BOLD, RESET, colorize
BANNER = r"""
...
"""
def parse_args():
    parser = argparse.ArgumentParser(...)
    parser.add_argument("--random", action="store_true", help="play with a random word instead of the daily word")
    parser.add_argument("--no-color", action="store_true", help="disable colored output")
    parser.add_argument("--date", type=str, default=None, help="play the daily word for a specific date (YYYY-MM-DD)")
    return parser.parse_args()
def print_instructions(): ...
def main():
    args = parse_args()
    set_color_enabled(not args.no_color)
    wm = WordManager()
    if args.random:
        answer = wm.get_random_word()
        mode = "random practice"
    else:
        date = parse date if given else today
        answer = wm.get_daily_word(date)
        mode = f"daily word for {date.isoformat()}"
    game = WordleGame(answer, wm)
    print banner, instructions
    print(f"Playing the {mode}. You have {MAX_ATTEMPTS} attempts.")
    while not game.is_over():
        print(game.render_board())
        try:
            guess = input("Enter guess: ")
        except (EOFError, KeyboardInterrupt):
            print("\nGame aborted.")
            reveal answer? maybe
            sys.exit(0)
        error = game.make_guess(guess)
        if error:
            print(colorize(error, RED-ish))
        else:
            print(game.render_board())  # hmm, printing board twice per turn?
    ...