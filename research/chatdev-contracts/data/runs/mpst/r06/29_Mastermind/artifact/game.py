'''
game.py
Core game engine for the Mastermind game.
`GameEngine` holds the secret code, validates the flow of the game
(attempts, win/lose conditions) and keeps the full guess history.
Feedback calculation itself lives in `feedback.py` so the engine stays
focused on game state.
'''
from feedback import calculate_feedback
class GuessRecord:
    """A single player guess together with the feedback it produced."""
    def __init__(self, guess, feedback):
        self.guess = list(guess)
        self.feedback = feedback
class GameEngine:
    """Runs one full round of Mastermind."""
    def __init__(self, secret_code, code_length, max_attempts, valid_symbols=None):
        if len(secret_code) != code_length:
            raise ValueError("Secret code length does not match code_length.")
        if max_attempts < 1:
            raise ValueError("max_attempts must be at least 1.")
        self.secret_code = list(secret_code)
        self.code_length = code_length
        self.max_attempts = max_attempts
        self.valid_symbols = set(valid_symbols) if valid_symbols is not None else None
        self.history = []
        self.won = False
        self.finished = False
    @property
    def attempts_used(self):
        return len(self.history)
    @property
    def attempts_remaining(self):
        return self.max_attempts - self.attempts_used
    def is_over(self):
        """True when the code is cracked or attempts are exhausted."""
        return self.finished
    def make_guess(self, guess):
        """
        Submit a guess.
        Returns the Feedback for the guess, updates the history and
        sets the win/lose state of the game.
        """
        if self.finished:
            raise RuntimeError("This game is already finished.")
        if len(guess) != self.code_length:
            raise ValueError(
                f"Guess must contain exactly {self.code_length} symbols."
            )
        if self.valid_symbols is not None and any(
            symbol not in self.valid_symbols for symbol in guess
        ):
            raise ValueError("Guess contains symbols that are not allowed.")
        feedback = calculate_feedback(guess, self.secret_code)
        self.history.append(GuessRecord(guess, feedback))
        if feedback.exact_matches == self.code_length:
            self.won = True
            self.finished = True
        elif self.attempts_used >= self.max_attempts:
            self.finished = True
        return feedback