'''
board.py
Rendering of the Mastermind game board.
Stores the history of guesses together with their feedback and renders
it as a table, so the player can review every previous attempt before
making the next one. Also renders the secret code for the end-of-round
reveal.
'''
from colors import letter_for, peg
from config import EMPTY_SYMBOL, EXACT_SYMBOL, PARTIAL_SYMBOL
class Board:
    """Holds and renders the history of guesses and their feedback."""
    def __init__(self, code_length, max_attempts):
        self.code_length = code_length
        self.max_attempts = max_attempts
        self.rows = []  # each row is a (guess, Feedback) tuple
    def add_row(self, guess, feedback):
        """Append one attempt (a guess and its feedback) to the board."""
        if len(guess) != self.code_length:
            raise ValueError(
                f"Guess has length {len(guess)}, expected {self.code_length}."
            )
        self.rows.append((list(guess), feedback))
    @property
    def attempts_used(self):
        """Number of guesses recorded so far."""
        return len(self.rows)
    @property
    def attempts_remaining(self):
        """Number of guesses the player has left."""
        return self.max_attempts - len(self.rows)
    def render(self):
        """Return the complete board as a printable multi-line string."""
        lines = []
        number_width = max(len(str(self.max_attempts)), 1)
        guess_width = self.code_length * 2 - 1  # letters separated by spaces
        feedback_width = max(self.code_length, len("Feedback"))
        header = (
            f"{'#':>{number_width}} | {'Guess':^{guess_width}} "
            f"| {'Feedback':^{feedback_width}}"
        )
        lines.append(header)
        lines.append("-" * len(header))
        if not self.rows:
            lines.append(
                f"{'-':>{number_width}} | {'(no guesses yet)':^{guess_width}} "
                f"| {'':^{feedback_width}}"
            )
        for index, (guess, feedback) in enumerate(self.rows, start=1):
            guess_text = " ".join(letter_for(c).upper() for c in guess)
            detail = feedback.as_symbols(
                EXACT_SYMBOL, PARTIAL_SYMBOL, EMPTY_SYMBOL, self.code_length
            )
            lines.append(f"{index:>{number_width}} | {guess_text} | {detail}")
        return "\n".join(lines)
    def render_secret(self, secret):
        """Render the hidden code for the end-of-round reveal."""
        return " ".join(peg(letter_for(c)) for c in secret)