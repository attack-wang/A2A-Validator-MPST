'''
game_logic.py
'''
from enum import Enum
class Feedback(Enum):
    GREEN = "green"
    YELLOW = "yellow"
    GREY = "grey"
MAX_ATTEMPTS = 6
WORD_LENGTH = 5
class GuessResult:
    def __init__(self, guess, feedback):
        self.guess = guess
        self.feedback = feedback  # list[Feedback]
    @property
    def is_win(self):
        return all(f == Feedback.GREEN for f in self.feedback)
class WordleGame:
    def __init__(self, answer, max_attempts=MAX_ATTEMPTS):
        self.answer = answer.lower()
        self.max_attempts = max_attempts
        self.history = []
        self._game_over = False
        self._won = False
    @property
    def attempts_used(self):
        return len(self.history)
    @property
    def attempts_remaining(self):
        return self.max_attempts - self.attempts_used
    @property
    def is_over(self):
        return self._game_over
    @property
    def won(self):
        return self._won
    def validate_format(self, raw_guess):
        """Return (is_valid, error_message)."""
        guess = raw_guess.strip().lower()
        if not guess:
            return False, "Empty input. Please type a 5-letter word."
        if len(guess) != WORD_LENGTH:
            return False, f"Your guess must be exactly {WORD_LENGTH} letters (you typed {len(guess)})."
        if not guess.isalpha():
            return False, "Guess may contain letters only (a-z)."
        return True, ""
    def make_guess(self, raw_guess):
        """Validate and record a guess. Returns (GuessResult|None, error_message)."""
        ok, err = self.validate_format(raw_guess)
        if not ok:
            return None, err
        guess = raw_guess.strip().lower()
        # dictionary check is done by caller (word_manager) or here via injected callable
        feedback = compute_feedback(guess, self.answer)
        result = GuessResult(guess, feedback)
        self.history.append(result)
        if result.is_win:
            self._won = True
            self._game_over = True
        elif self.attempts_used >= self.max_attempts:
            self._game_over = True
        return result, ""