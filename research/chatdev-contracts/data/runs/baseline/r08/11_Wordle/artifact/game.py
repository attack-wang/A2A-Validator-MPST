'''
game.py
Contains the WordleGame class, which encapsulates the rules and state of a
single Wordle round:
  - 6 attempts to guess a 5-letter word
  - guesses must be valid 5-letter dictionary words
  - each guess produces per-letter color feedback (green/yellow/grey)
'''
from feedback import evaluate_guess
class WordleGame:
    MAX_ATTEMPTS = 6
    WORD_LENGTH = 5
    def __init__(self, target, valid_words):
        self.target = target.lower()
        self.valid_words = valid_words
        self.guesses = []
        self.feedbacks = []
    def is_valid_guess(self, guess):
        if len(guess) != self.WORD_LENGTH: return False
        if not guess.isalpha(): return False
        return guess.lower() in self.valid_words
    def validation_error(self, guess):
        if len(guess) != self.WORD_LENGTH:
            return f"Guess must be exactly {self.WORD_LENGTH} letters."
        if not guess.isalpha():
            return "Guess must contain only letters."
        if guess.lower() not in self.valid_words:
            return f"'{guess.upper()}' is not in the word list."
        return None
    def submit_guess(self, guess):
        guess = guess.strip().lower()
        error = self.validation_error(guess)
        if error:
            return None, error
        feedback = evaluate_guess(guess, self.target)
        self.guesses.append(guess)
        self.feedbacks.append(feedback)
        return feedback, None
    def is_won(self):
        return bool(self.guesses) and self.guesses[-1] == self.target
    def is_finished(self):
        return self.is_won() or len(self.guesses) >= self.MAX_ATTEMPTS
    def attempts_used(self):
        return len(self.guesses)
    def attempts_remaining(self):
        return self.MAX_ATTEMPTS - len(self.guesses)