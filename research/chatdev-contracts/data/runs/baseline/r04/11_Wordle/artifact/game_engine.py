'''
game_engine.py
'''
from feedback import evaluate_guess, GuessFeedback
class WordleGame:
    MAX_ATTEMPTS = 6
    WORD_LENGTH = 5
    def __init__(self, answer, max_attempts=MAX_ATTEMPTS):
        self.answer = answer.upper()
        self.max_attempts = max_attempts
        self.history = []  # list of GuessFeedback
    @property
    def attempts_used(self):
        return len(self.history)
    @property
    def attempts_remaining(self):
        return self.max_attempts - self.attempts_used
    @property
    def is_won(self):
        return bool(self.history) and self.history[-1].is_correct
    @property
    def is_over(self):
        return self.is_won or self.attempts_used >= self.max_attempts
    def make_guess(self, guess):
        """Record and evaluate a guess; returns GuessFeedback.
        Raises ValueError if the game is over."""
        if self.is_over:
            raise ValueError("The game is already over.")
        guess = guess.strip().upper()
        if len(guess) != self.WORD_LENGTH:
            raise ValueError(f"Guess must be exactly {self.WORD_LENGTH} letters.")
        if not guess.isalpha():
            raise ValueError("Guess may contain letters only.")
        result = evaluate_guess(guess, self.answer)
        self.history.append(result)
        return result