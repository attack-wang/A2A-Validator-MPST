'''
game_engine.py
'''
from feedback_renderer import Feedback  # or define states here
class GameEngine:
    MAX_ATTEMPTS = 6
    WORD_LENGTH = 5
    def __init__(self, answer, max_attempts=MAX_ATTEMPTS):
        self.answer = answer.lower()
        self.max_attempts = max_attempts
        self.guesses = []       # list of guess strings
        self.feedbacks = []     # list of feedback lists
        self.won = False
    def validate_guess(self, guess):
        guess = guess.strip().lower()
        if len(guess) != WORD_LENGTH: return (False, "...")
        if not guess.isalpha(): return (False, "...")
        return (True, "")
    def evaluate_guess(self, guess):
        # returns list of Feedback states
        ...
    def submit_guess(self, guess):
        feedback = self.evaluate_guess(guess)
        self.guesses.append(guess)
        self.feedbacks.append(feedback)
        if guess == self.answer:
            self.won = True
        return feedback
    @property
    def attempts_used(self): return len(self.guesses)
    @property
    def attempts_left(self): return self.max_attempts - len(self.guesses)
    @property
    def is_over(self): return self.won or len(self.guesses) >= self.max_attempts