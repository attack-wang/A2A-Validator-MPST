'''
Entry point: parse arguments, wire components together, start the game.
'''
import argparse
from colors import supports_color
from feedback import LetterResult  # not needed here actually
from validator import GuessValidator
from word_manager import WordManager
from game import WordleGame
import ui
def parse_args():
    parser = argparse.ArgumentParser(description="Play Wordle in your Linux terminal.")
    parser.add_argument("--no-color", action="store_true", help="disable ANSI colors")
    parser.add_argument("--date", type=str, default=None, help="YYYY-MM-DD to play the daily word of that date")
    parser.add_argument("--word", type=str, default=None, help="override the answer (for testing)")
    return parser.parse_args()
def main():
    args = parse_args()
    use_color = supports_color() and not args.no_color
    ui.print_banner(use_color)
    word_manager = WordManager()
    validator = GuessValidator(word_manager.valid_guesses)
    play_date = None
    if args.date:
        try:
            from datetime import date
            y, m, d = (int(p) for p in args.date.split("-"))
            play_date = date(y, m, d)
        except ValueError:
            print("Invalid --date, expected YYYY-MM-DD.")
            return
    answer = args.word.lower() if args.word else None
    if answer is not None and len(answer) != 5:
        print("--word must be a 5-letter word.")
        return
    game = WordleGame(word_manager, validator, answer=answer, use_color=use_color)
    game.play()
if __name__ == "__main__":
    main()