'''
game.py
Core game engine for the Mastermind game.
Handles secret generation, attempt tracking, guess validation,
win/lose determination, and delegates scoring to feedback.py.
'''
import random
from feedback import calculate_feedback
class MastermindGame:
    """Encapsulates all state and rules of one Mastermind session."""
    COLORS = ['red', 'blue', 'green', 'yellow', 'orange', 'purple',
              'pink', 'brown']
    def __init__(self, code_length=4, num_colors=6, max_attempts=10):
        """Create a new game: generate the secret code and reset state."""
        if not (1 <= num_colors <= len(self.COLORS)):
            raise ValueError("num_colors out of range.")
        if code_length < 1:
            raise ValueError("code_length must be at least 1.")
        if max_attempts < 1:
            raise ValueError("max_attempts must be at least 1.")
        self.code_length = code_length
        self.max_attempts = max_attempts
        self._attempts_used = 0
        self._won = False
        self._finished = False
        self.history = []  # list of (guess_tuple, (exact, partial))
        self.palette = self.COLORS[:num_colors]
        # random.choices allows duplicate colors in the secret (classic rules)
        self._secret = tuple(random.choices(self.palette, k=code_length))
    def submit_guess(self, guess):
        """Validate and submit a guess; return (exact, partial) feedback."""
        if self.is_over():
            raise RuntimeError("Game is already over. Start a new game.")
        guess = tuple(guess)
        if len(guess) != self.code_length:
            raise ValueError("Guess must have exactly {} colors.".format(self.code_length))
        for color in guess:
            if color not in self.palette:
                raise ValueError("Invalid color: {}".format(color))
        exact, partial = calculate_feedback(self._secret, guess)
        self._attempts_used += 1
        self.history.append((guess, (exact, partial)))
        if exact == self.code_length:
            self._won = True
            self._finished = True
        elif self._attempts_used >= self.max_attempts:
            self._finished = True
        return exact, partial
    def is_over(self):
        """Return True when the game is won or attempts are exhausted."""
        return self._finished
    def is_won(self):
        """Return True only if the player cracked the code."""
        return self._won
    def attempts_remaining(self):
        """Return the number of guesses the player has left."""
        return self.max_attempts - self._attempts_used
    def attempts_used(self):
        """Return the number of guesses already made."""
        return self._attempts_used
    def reveal_secret(self):
        """Return the hidden code (call only after game over in the UI)."""
        return self._secret
    def get_palette(self):
        """Return the list of colors available for guessing."""
        return list(self.palette)