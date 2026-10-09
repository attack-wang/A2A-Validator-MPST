'''
board.py
The guess board: stores every guess together with its feedback and renders
the whole board as text so the player can review previous attempts.
Rendering conventions:
  * colored ●  -> the guessed peg (color taken from the palette)
  * ●          -> exact match feedback (right color, right position)
  * ○          -> partial match feedback (right color, wrong position)
  * dim ·      -> unused slot
'''
from colors import DIM, RESET
from textutils import pad, visible_width
class Board:
    """History of guesses and feedback for one round, plus text rendering."""
    def __init__(self, code_length, max_attempts):
        self.code_length = code_length
        self.max_attempts = max_attempts
        self.rows = []  # list of (guess, exact, partial)
    def add_guess(self, guess, exact, partial):
        """Record one evaluated guess."""
        self.rows.append((list(guess), exact, partial))
    def is_full(self):
        return len(self.rows) >= self.max_attempts
    def _peg_row(self, guess, palette):
        return " ".join(palette.get(index).peg() for index in guess)
    def _feedback_row(self, exact, partial):
        pegs = ["●"] * exact + ["○"] * partial
        pegs += [f"{DIM}·{RESET}"] * (self.code_length - len(pegs))
        return " ".join(pegs)
    def _empty_peg_row(self):
        return " ".join([f"{DIM}·{RESET}"] * self.code_length)
    def render(self, palette):
        """Return the full board (header + every attempt) as a string."""
        number_width = max(2, len(str(self.max_attempts)))
        guess_width = 2 * self.code_length - 1
        lines = []
        header = (
            f" {'#':>{number_width}} | {'GUESS':^{guess_width}} | FEEDBACK"
        )
        lines.append(header)
        lines.append("-" * visible_width(header))
        for attempt, (guess, exact, partial) in enumerate(self.rows, start=1):
            lines.append(
                f" {str(attempt):>{number_width}} | "
                f"{pad(self._peg_row(guess, palette), guess_width)} | "
                f"{self._feedback_row(exact, partial)}"
            )
        for attempt in range(len(self.rows) + 1, self.max_attempts + 1):
            lines.append(
                f" {str(attempt):>{number_width}} | "
                f"{pad(self._empty_peg_row(), guess_width)} | "
                f"{self._feedback_row(0, 0)}"
            )
        return "\n".join(lines)