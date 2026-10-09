'''
game.py
Core Wordle game engine and terminal rendering.
Defines MAX_ATTEMPTS (6) and the WordleGame class, which owns the
complete game loop:
  - prints a header explaining the color rules,
  - renders the board (past guesses plus empty rows) and the
    on-screen keyboard with per-letter status,
  - reads guesses from the player; invalid guesses print an error
    and do not consume an attempt,
  - applies per-letter feedback (GREEN / YELLOW / GREY) using the
    official duplicate-letter rules,
  - finishes by announcing a win or revealing the secret word.
'''
from colors import Colors, GREEN, YELLOW, GREY, colorize, tile, row
from validator import WORD_LENGTH
MAX_ATTEMPTS = 6
class WordleGame:
    """One round of terminal Wordle."""
    def __init__(self, target_word, validator, output_fn=print, input_fn=input):
        self.target_word = target_word.upper()
        self.validator = validator
        self.output_fn = output_fn
        self.input_fn = input_fn
        self.history = []  # list of (guess, feedback) tuples
        self.won = False
    # ---------------- state helpers ---------------- #
    @property
    def attempts_left(self):
        """Number of guesses the player still has."""
        return MAX_ATTEMPTS - len(self.history)
    def is_over(self):
        """True when the word was guessed or all attempts are used."""
        return self.won or len(self.history) >= MAX_ATTEMPTS
    # ---------------- turn handling ---------------- #
    def take_turn(self, raw_guess):
        """
        Validate the raw guess; if valid, record it with feedback and
        check for a win. Invalid guesses print an error and do not
        consume an attempt. Returns the feedback list or None.
        """
        ok, error = self.validator.validate(raw_guess)
        if not ok:
            self.output_fn(colorize(f"  ✗ {error}", Colors.RED))
            return None
        guess = raw_guess.strip().upper()
        feedback = self.validator.evaluate(guess, self.target_word)
        self.history.append((guess, feedback))
        if guess == self.target_word:
            self.won = True
        return feedback
    # ---------------- rendering ---------------- #
    def print_header(self):
        """Print the title banner and the color-rule legend."""
        self.output_fn(colorize("=" * 46, Colors.CYAN))
        self.output_fn(colorize("  TERMINAL WORDLE", Colors.CYAN + Colors.BOLD))
        self.output_fn(colorize(f"  Guess the {WORD_LENGTH}-letter word in {MAX_ATTEMPTS} tries.", Colors.CYAN))
        self.output_fn("  " + tile("G", GREEN) + colorize(" green  = right letter, right spot", Colors.WHITE))
        self.output_fn("  " + tile("Y", YELLOW) + colorize(" yellow = right letter, wrong spot", Colors.WHITE))
        self.output_fn("  " + tile("G", GREY) + colorize(" grey   = letter not in the word", Colors.WHITE))
        self.output_fn(colorize("  Type 'quit' (or Ctrl+C) to exit early.", Colors.DIM))
        self.output_fn(colorize("=" * 46, Colors.CYAN))