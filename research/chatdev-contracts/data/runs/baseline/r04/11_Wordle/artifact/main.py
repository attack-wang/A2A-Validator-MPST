'''
main.py — entry point
'''
import argparse
import datetime
import sys
from word_manager import WordManager
from game_engine import WordleGame
from input_handler import InputHandler
import display
def parse_args(argv=None):
    parser = argparse.ArgumentParser(...)
    parser.add_argument("--word", help="override the daily word (for testing)")
    parser.add_argument("--date", help="ISO date (YYYY-MM-DD) to play another day's puzzle")
    parser.add_argument("--seed", type=int, help="random word instead of daily (for testing)")
    return parser.parse_args(argv)
def run_game(word_manager, answer, io):
    game = WordleGame(answer)
    display.print_welcome(...)
    display.print_rules()
    while not game.is_over:
        display.print_attempts_remaining(game)
        guess = io.get_guess()
        result = game.make_guess(guess)
        display.print_board(game.history)
        display.print_keyboard(game.history)
        if game.is_won:
            display.print_win(...)
            return 0
    display.print_lose(answer)
    return 1
def main(argv=None):
    args = parse_args(argv)
    display.enable_ansi()
    word_manager = WordManager()
    if args.word:
        answer = args.word.strip().lower()
        validate 5 letters alpha else error
    elif args.seed is not None:
        random.seed(args.seed); answer = word_manager.get_random_word()
    elif args.date:
        parse date; answer = word_manager.get_daily_word(date)
    else:
        answer = word_manager.get_daily_word()
    return run_game(word_manager, answer, InputHandler(word_manager))
if __name__ == "__main__":
    sys.exit(main())