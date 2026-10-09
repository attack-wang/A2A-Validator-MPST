'''
wordle_game.py
Core Wordle state machine: tracks the secret answer, the player's
guess history, remaining attempts and win/lose conditions.
'''
from feedback import evaluate_guess, LetterState
WORD_LENGTH = 5
MAX_ATTEMPTS = 6
class GuessError(Exception):
    '''Raised when a guess fails validation; carries a player-facing reason.'''
    def __init__(self, reason):
        super().__init__(reason)
        self.reason = reason
class WordleGame:
    '''One round of Wordle (answer + up to MAX_ATTEMPTS guesses).'''
    def __init__(self, answer, max_attempts=MAX_ATTEMPTS, word_validator=None):
        answer = answer.strip().lower()
        if len(answer) != WORD_LENGTH or not answer.isalpha():
            raise ValueError(...)
        self.answer = answer
        self.max_attempts = max_attempts
        self._validator = word_validator
        self.guesses = []      # list of guess strings
        self.history = []      # list of (guess, [LetterState]) tuples
    def validate_guess(self, guess):
        '''Raise GuessError with a friendly reason if the guess is illegal.'''
        guess = guess.strip().lower()
        if not guess:
            raise GuessError("Empty input — please type a 5-letter word.")
        if not guess.isalpha():
            raise GuessError("Guess must contain only letters A–Z.")
        if len(guess) != WORD_LENGTH:
            raise GuessError(f"Guess must be exactly {WORD_LENGTH} letters (you typed {len(guess)}).")
        if self._validator is not None and not self._validator(guess):
            raise GuessError(f"'{guess.lower()}' is not in our word list.")
        return guess
    def submit_guess(self, guess):
        '''
        Validate, record and score a guess.
        Returns (states, finished) or just states? Let me return states list.
        Raises GuessError on invalid input.
        '''
        guess = self.validate_guess(guess)
        states = evaluate_guess(guess, self.answer)
        self.guesses.append(guess)
        self.history.append((guess, states))
        return states
    def is_won(self):
        return bool(self.history) and self.history[-1][0] == self.answer
    def is_finished(self):
        return self.is_won() or self.attempts_used() >= self.max_attempts
    def attempts_used(self):
        return len(self.history)
    def remaining_attempts(self):
        return self.max_attempts - self.attempts_used()