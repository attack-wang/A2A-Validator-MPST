'''
main.py
Entry point for the terminal-based Wordle game. Handles the game loop,
input validation, win/lose logic, and screen refreshing.
Robustness notes:
  - The screen is only cleared on real terminals, so redirected/piped
    output stays intact.
  - Command-line flags are validated; --help shows usage.
  - Unexpected errors are reported gracefully instead of dumping a traceback.
Usage:
    python3 main.py           # play with today's daily word
    python3 main.py --random  # play with a random word
    python3 main.py --help    # show usage information
'''
import os
import sys
from wordlist import get_daily_word, get_random_word, is_valid_word
from feedback import evaluate_guess, BOLD, RESET
from board import Board
MAX_ATTEMPTS = 6
WORD_LENGTH = 5
ALLOWED_LETTERS = set("abcdefghijklmnopqrstuvwxyz")
QUIT_COMMANDS = ("q", "quit", "exit")
class Game:
    """Represents a single session of the Wordle game."""
    def __init__(self, answer):
        self.answer = answer.lower()
        self.board = Board(max_attempts=MAX_ATTEMPTS)
        self.guesses = 0
        self.won = False
    def print_header(self):
        """Print the game title and instructions."""
        print("=" * 40)
        print(f"{BOLD}  W O R D L E  -  Linux Terminal Edition{RESET}")
        print("=" * 40)
        print("Guess the 5-letter word in 6 attempts.")
        print("Colors: GREEN = correct letter & position,")
        print("        YELLOW = correct letter, wrong position,")
        print("        GREY = letter not in the word.")
        print("Type 'q' to quit. Flags: --random for random word.")
        print("-" * 40)
    def prompt_guess(self, attempt):
        """Prompt the user until a valid 5-letter dictionary word is entered."""
        while True:
            try:
                raw = input(
                    f"Attempt {attempt}/{MAX_ATTEMPTS} - Enter a 5-letter word: "
                ).strip().lower()
            except (EOFError, KeyboardInterrupt):
                print("\nThanks for playing! Goodbye.")
                sys.exit(0)
            if raw in QUIT_COMMANDS:
                print("Thanks for playing! Goodbye.")
                sys.exit(0)
            if len(raw) != WORD_LENGTH:
                print(f"Error: your guess must be exactly {WORD_LENGTH} letters long.")
                continue
            # Strict a-z check: str.isalpha() alone also accepts accented
            # Unicode letters such as 'é', which are never valid guesses.
            if not all(ch in ALLOWED_LETTERS for ch in raw):
                print("Error: your guess must contain only letters a-z.")
                continue
            if not is_valid_word(raw):
                print("Error: word not in the dictionary. Try another word.")
                continue
            return raw
    def refresh_screen(self):
        """Clear the terminal and redraw header plus current board state."""
        # Only clear real terminals; when output is piped or redirected,
        # clearing would destroy the transcript, so we simply reprint.
        if sys.stdout.isatty():
            os.system("clear" if os.name != "nt" else "cls")
        self.print_header()
        print(self.board.render())
    def print_result(self):
        """Print the final win/lose message, revealing the word if needed."""
        print("-" * 40)
        if self.won:
            print(
                f"Congratulations! You guessed the word "
                f"'{self.answer.upper()}' in {self.guesses} attempt(s). You win!"
            )
        else:
            print(
                f"Game over! You used all {MAX_ATTEMPTS} attempts. "
                f"The word was '{self.answer.upper()}'. Better luck tomorrow!"
            )
        print("=" * 40)
    def play(self):
        """Run the main game loop."""
        self.print_header()
        print(self.board.render())
        while self.guesses < MAX_ATTEMPTS and not self.won:
            guess = self.prompt_guess(self.guesses + 1)
            evaluated = evaluate_guess(guess, self.answer)
            self.board.add_row(evaluated)
            self.guesses += 1
            self.refresh_screen()
            if guess == self.answer:
                self.won = True
        self.print_result()
def choose_answer():
    """Pick the answer word: daily word by default, random if --random flag given."""
    if "--random" in sys.argv or "-r" in sys.argv:
        return get_random_word()
    return get_daily_word()
def print_usage():
    """Print command-line usage information."""
    print("Usage: python3 main.py [--random | -r] [--help | -h]")
    print("  (default)  Play with today's deterministic daily word.")
    print("  --random   Play with a randomly chosen word.")
    print("  --help     Show this help message and exit.")
def main():
    """Program entry point with graceful top-level error handling."""
    if "--help" in sys.argv or "-h" in sys.argv:
        print_usage()
        return
    try:
        answer = choose_answer()
        Game(answer).play()
    except KeyboardInterrupt:
        print("\nThanks for playing! Goodbye.")
    except Exception as exc:
        print(f"Unexpected error: {exc}", file=sys.stderr)
        sys.exit(1)
if __name__ == "__main__":
    main()