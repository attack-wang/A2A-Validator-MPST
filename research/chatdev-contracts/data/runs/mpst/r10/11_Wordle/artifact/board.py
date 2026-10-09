'''
board.py
Renders the Wordle board in the terminal using ANSI colors from colors.py.
Draws the guess grid with colored tiles, empty slots, and end-of-game banners.
'''
from colors import (BG_GREEN, BG_GREY, BG_YELLOW, BOLD, DIM, FG_GREEN, FG_RED,
                    FG_WHITE, colorize, tile)
from game_logic import LetterState
STATE_TO_BG = {
    LetterState.GREEN: BG_GREEN,
    LetterState.YELLOW: BG_YELLOW,
    LetterState.GREY: BG_GREY,
}
HEADER = (
    "=== WORDLE (Terminal Edition) ===\n"
    "Guess the 5-letter word in 6 tries.\n"
    "- Green  : right letter, right spot\n"
    "- Yellow : right letter, wrong spot\n"
    "- Grey   : letter not in the word\n"
    "Type your guess and press Enter. (Ctrl+C to quit)"
)
WIN_MESSAGES = ["Genius", "Magnificent", "Impressive", "Splendid", "Great", "Phew"]
class Board:
    """Draws the guess grid, empty slots, and end-of-game messages."""
    def __init__(self, word_length=5, max_attempts=6):
        self._word_length = word_length
        self._max_attempts = max_attempts
    def show_header(self):
        print(HEADER)
    def show_board(self, game):
        print()
        for guess, feedback in zip(game.guesses, game.feedback_history):
            print(" ".join(tile(ch, STATE_TO_BG[state])
                           for ch, state in zip(guess, feedback)))
        for _ in range(game.attempts_remaining):
            print(" ".join(colorize(" _ ", DIM, FG_WHITE)
                           for _ in range(self._word_length)))
        print()
    def show_win(self, game):
        msg = WIN_MESSAGES[min(game.attempts_used, len(WIN_MESSAGES)) - 1]
        print(colorize(f"\n{msg}! You got it in {game.attempts_used}/{self._max_attempts}.",
                       BOLD, FG_GREEN))
    def show_loss(self, game):
        print(colorize(f"\nOut of attempts. The word was: {game.answer.upper()}",
                       BOLD, FG_RED))