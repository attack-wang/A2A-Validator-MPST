'''
ui.py
Console user interface for the Mastermind game.
The ConsoleUI class renders the game board, prompts the player for
guesses, displays feedback (exact/partial pegs), win/lose/forfeit
outcomes, and handles replay. It degrades gracefully: falls back to
ASCII peg symbols when Unicode is unavailable and disables ANSI color
when stdout is not a terminal.
'''
import sys
from colors import colorize, supports_unicode
from feedback import format_feedback, EXACT_PEG, PARTIAL_PEG, MISS_PEG
class ConsoleUI:
    """Console rendering and input handling for one MastermindGame."""
    def __init__(self, game):
        self.game = game
        self.use_unicode = supports_unicode()
        self.use_color = sys.stdout.isatty()
        # ASCII fallback pegs used when Unicode symbols can't be encoded.
        self.pegs = {"exact": "X", "partial": "o", "miss": "-"}
    # ------------------------------------------------------------------
    # Low-level rendering helpers
    # ------------------------------------------------------------------
    def _peg_string(self, exact, partial):
        """Render feedback counts as a peg string in supported symbols."""
        code_length = self.game.code_length
        if self.use_unicode:
            return format_feedback(exact, partial, code_length)
        pegs = self.pegs["exact"] * exact + self.pegs["partial"] * partial
        return pegs + self.pegs["miss"] * (code_length - exact - partial)
    def _render_code(self, letters):
        """Render a code or guess as (colored) space-separated letters."""
        if self.use_color:
            return " ".join(colorize(ch, ch) for ch in letters)
        return " ".join(letters)
    def _render_history_row(self, guess, exact, partial):
        """Render one history row: guess letters + feedback pegs."""
        return f"  {self._render_code(guess)}  |  {self._peg_string(exact, partial)}"
    def _peg_legend(self):
        """Return (exact, partial, miss) symbols supported on this console."""
        if self.use_unicode:
            return EXACT_PEG, PARTIAL_PEG, MISS_PEG
        return self.pegs["exact"], self.pegs["partial"], self.pegs["miss"]
    # ------------------------------------------------------------------
    # Screens / messages
    # ------------------------------------------------------------------
    def show_welcome(self):
        """Explain the rules and show the active color palette."""
        exact, partial, miss = self._peg_legend()
        print("=" * 52)
        print(f"Crack the secret code of {self.game.code_length} colors!")
        print(f"You have {self.game.max_attempts} attempts. Colors may repeat.")
        print("Available colors:")
        palette_line = ",  ".join(
            f"{self._render_code(letter)} = {name}"
            for letter, name in self.game.palette_names()
        )
        print(f"  {palette_line}")
        print("Feedback after each guess:")
        print(f"  {exact} = exact match (right color, right position)")
        print(f"  {partial} = partial match (right color, wrong position)")
        print(f"  {miss} = color not in the code")
        print("=" * 52)
    def show_board(self):
        """Print all guesses so far with their feedback pegs."""
        print()
        print("  CURRENT BOARD")
        print("  " + "-" * 46)
        for i, (guess, exact, partial) in enumerate(self.game.history, start=1):
            print(f"  {i:>2}. {self._render_history_row(guess, exact, partial)}")
        if self.game.history:
            print("  " + "-" * 46)
        if not self.game.is_over():
            print(f"  Attempts used: {self.game.attempts_used}/{self.game.max_attempts} "
                  f"({self.game.remaining_attempts()} remaining)")
    def show_round_header(self):
        """Announce the upcoming attempt."""
        print(f"\n--- Attempt {self.game.attempts_used + 1} "
              f"of {self.game.max_attempts} ---")
    def get_guess(self):
        """
        Prompt until the player enters a valid guess.
        Returns the cleaned guess string, or None when the player gives
        up (types QUIT, or presses Ctrl+C / EOF).
        """
        example = "".join(self.game.palette[: self.game.code_length])
        prompt = f"Enter your guess (e.g. {example}) or 'QUIT' to give up: "
        while True:
            try:
                raw = input(prompt).strip()
            except (EOFError, KeyboardInterrupt):
                print()
                return None
            if raw.upper() == "QUIT":
                return None
            valid, error = self.game.is_valid_guess(raw)
            if valid:
                return raw.strip().upper()
            print(f"  Invalid guess: {error}")
    def show_win(self):
        """Celebrate a solved code."""
        print("\n" + "*" * 52)
        print("*** CONGRATULATIONS! You cracked the code! ***")
        print(f"Solved in {self.game.attempts_used} of "
              f"{self.game.max_attempts} attempts.")
        print(f"The secret code was: {self._render_code(self.game.reveal_secret())}")
        print("*" * 52)
    def show_lose(self):
        """Reveal the secret after the attempts run out."""
        print("\n" + "-" * 52)
        print("GAME OVER — you ran out of attempts!")
        print(f"The secret code was: {self._render_code(self.game.reveal_secret())}")
        print("-" * 52)
    def show_forfeit(self):
        """Reveal the secret after the player gives up."""
        print("\n" + "-" * 52)
        print("You gave up — better luck next time!")
        print(f"The secret code was: {self._render_code(self.game.reveal_secret())}")
        print("-" * 52)
    def ask_play_again(self):
        """Ask whether to start another game; returns True/False."""
        while True:
            try:
                answer = input("Play again? [y/n]: ").strip().lower()
            except (EOFError, KeyboardInterrupt):
                print()
                return False
            if answer in ("y", "yes"):
                return True
            if answer in ("n", "no", ""):
                return False
            print("  Please answer 'y' or 'n'.")