'''
game.py
Core Mastermind game orchestration: runs one full round of Mastermind.
Handles round setup (secret code, palette legend, history board), the
guess loop with input validation and duplicate-safe feedback, and the
final win/lose/abort outcome with a reveal of the hidden code.
'''
from config import COLOR_LETTERS, COLOR_NAMES, EXACT_PEG, PARTIAL_PEG
from secret_code import SecretCode
from feedback import calculate_feedback
from validator import parse_guess, QuitGame
from history import GameHistory
from ui import banner, clear_screen, paint_color_letter
class MastermindGame:
    """Orchestrates a single round: setup, guess loop, feedback, outcome."""
    def __init__(self, difficulty):
        self.difficulty = difficulty
        self.palette = COLOR_LETTERS[:difficulty.palette_size]
        self.palette_names = COLOR_NAMES[:difficulty.palette_size]
        self.code_length = difficulty.code_length
        self.max_attempts = difficulty.max_attempts
        self.secret = SecretCode(self.palette, self.code_length,
                                 allow_duplicates=difficulty.allow_duplicates)
        self.history = GameHistory()
    def _print(self, text=""):
        """Central output helper for the round."""
        print(text)
    def _show_palette(self):
        """Display the available colors as a tinted letter=name legend."""
        legend = ", ".join(f"{paint_color_letter(letter)} = {name}"
                           for letter, name in zip(self.palette, self.palette_names))
        self._print(f"Colors: {legend}")
    def play(self):
        """Run the game loop until win/lose/quit and report the outcome."""
        self._print(clear_screen())
        self._print(banner())
        self._print(f"Crack the hidden {self.code_length}-color code in "
                    f"{self.max_attempts} attempts. Type 'q' to quit.")
        self._show_palette()
        self._print(f"Feedback: {EXACT_PEG} = right color & position, "
                    f"{PARTIAL_PEG} = right color, wrong position.")
        won = aborted = False
        while len(self.history) < self.max_attempts:
            attempt = len(self.history) + 1
            try:
                raw = input(f"\nAttempt {attempt}/{self.max_attempts}: ")
            except (EOFError, KeyboardInterrupt):
                self._print()
                aborted = True
                break
            try:
                guess, error = parse_guess(raw, self.palette, self.code_length)
            except QuitGame:
                aborted = True
                break
            if error:
                self._print(f"  ✗ {error}")
                continue
            feedback = calculate_feedback(guess, self.secret.code)
            self.history.add(attempt, guess, feedback)
            self._print(self.history.render(self.code_length, self.max_attempts))
            if feedback.is_win:
                won = True
                break
        self._print()
        if won:
            self._print(f"🎉 You cracked the code in {len(self.history)} attempt(s)!")
        elif aborted:
            self._print("Game aborted.")
        else:
            self._print("Out of attempts — you lose!")
        revealed = " ".join(paint_color_letter(letter) for letter in self.secret.code)
        self._print(f"The secret code was: {revealed}")
        return won