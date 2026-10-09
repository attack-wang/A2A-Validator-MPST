'''
main.py
Entry point for the terminal Wordle game. Wires together the word manager,
game logic and board renderer, and runs the interactive game loop.
'''
import argparse
import sys
from board import Board
from game_logic import WordleGame
from word_manager import WordManager
def parse_arguments(argv=None):
    parser = argparse.ArgumentParser(description="Play Wordle in your Linux terminal.")
    parser.add_argument("--random", action="store_true",
                        help="play with a random word instead of today's daily word")
    return parser.parse_args(argv)
def read_guess(attempt, max_attempts):
    try:
        return input(f"Guess {attempt}/{max_attempts}: ")
    except (EOFError, KeyboardInterrupt):
        print("\nGoodbye!")
        sys.exit(0)
def main():
    args = parse_arguments()
    manager = WordManager()
    answer = manager.get_random_word() if args.random else manager.get_daily_word()
    game = WordleGame(answer, validator=manager.is_valid_guess)
    board = Board(word_length=game.WORD_LENGTH, max_attempts=game.MAX_ATTEMPTS)
    board.show_header()
    board.show_board(game)
    while not game.is_over:
        raw = read_guess(game.attempts_used + 1, game.MAX_ATTEMPTS)
        error = game.validate_guess(raw)
        if error:
            print(error)
            continue
        game.make_guess(raw.strip().lower())
        board.show_board(game)
    if game.is_won:
        board.show_win(game)
    else:
        board.show_loss(game)
if __name__ == "__main__":
    main()