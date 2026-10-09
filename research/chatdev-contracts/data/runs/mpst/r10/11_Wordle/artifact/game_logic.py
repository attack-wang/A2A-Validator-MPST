'''
game_logic.py
Core Wordle rules: guess evaluation with duplicate-letter handling and game state tracking.
'''
from enum import Enum
class LetterState(Enum):
    GREEN = "green"
    YELLOW = "yellow"
    GREY = "grey"
class WordleGame:
    MAX_ATTEMPTS = 6
    WORD_LENGTH = 5
    def __init__(self, answer, max_attempts=MAX_ATTEMPTS, validator=None):
        self._answer = answer.lower()
        self._max_attempts = max_attempts
        self._validator = validator
        self._guesses = []
        self._feedback_history = []
    @property
    def answer(self):
        return self._answer
    @property
    def guesses(self):
        return tuple(self._guesses)
    @property
    def feedback_history(self):
        return tuple(self._feedback_history)
    @property
    def attempts_used(self):
        return len(self._guesses)
    @property
    def attempts_remaining(self):
        return self._max_attempts - self.attempts_used
    @property
    def is_won(self):
        return bool(self._guesses) and self._guesses[-1] == self._answer
    @property
    def is_over(self):
        return self.is_won or self.attempts_used >= self._max_attempts
    @staticmethod
    def evaluate_guess(guess, answer):
        """Two-pass evaluation: greens first, then yellows against remaining letter counts."""
        feedback = [LetterState.GREY] * len(answer)
        remaining = {}
        for i, (g_char, a_char) in enumerate(zip(guess, answer)):
            if g_char == a_char:
                feedback[i] = LetterState.GREEN
            else:
                remaining[a_char] = remaining.get(a_char, 0) + 1
        for i, g_char in enumerate(guess):
            if feedback[i] == LetterState.GREEN:
                continue
            if remaining.get(g_char, 0) > 0:
                feedback[i] = LetterState.YELLOW
                remaining[g_char] -= 1
        return tuple(feedback)
    def validate_guess(self, raw_guess):
        guess = raw_guess.strip().lower()
        if len(guess) != self.WORD_LENGTH:
            return f"Please enter exactly {self.WORD_LENGTH} letters."
        if not guess.isalpha():
            return "Only alphabetic characters are allowed."
        if self._validator and not self._validator(guess):
            return "Not in the word list. Try another word."
        return None
    def make_guess(self, guess):
        guess = guess.lower()
        feedback = self.evaluate_guess(guess, self._answer)
        self._guesses.append(guess)
        self._feedback_history.append(feedback)
        return feedback