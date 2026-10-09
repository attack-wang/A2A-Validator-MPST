'''
game_engine.py
Core game logic for Mastermind.
The GameEngine owns the hidden secret code, evaluates player guesses and
produces the classic black/white peg feedback:
  * exact   -> right color in the right position  (black peg ●)
  * partial -> right color in the wrong position  (white peg ○)
The counting algorithm never double-counts: a peg that is already an exact
match is removed from both sequences before partial matches are tallied.
'''
import random
from collections import Counter
class GameEngine:
    """State and rules of a single Mastermind round."""
    def __init__(self, difficulty, rng=None):
        self.code_length = difficulty.code_length
        self.palette_size = difficulty.palette_size
        self.max_attempts = difficulty.max_attempts
        self.allow_duplicates = difficulty.allow_duplicates
        self.rng = rng if rng is not None else random.Random()
        self.secret = self._generate_secret()
        self.attempts_used = 0
        self.solved = False
    def _generate_secret(self):
        """Randomly build the hidden code according to the difficulty rules."""
        if self.allow_duplicates:
            return [self.rng.randrange(self.palette_size) for _ in range(self.code_length)]
        return self.rng.sample(range(self.palette_size), self.code_length)
    def is_valid_guess(self, guess):
        """True when `guess` is a list of palette indices of the right length."""
        return (
            isinstance(guess, list)
            and len(guess) == self.code_length
            and all(isinstance(g, int) and 0 <= g < self.palette_size for g in guess)
        )
    def evaluate_guess(self, guess):
        """Score one guess.
        Returns (exact, partial). Raises ValueError for malformed guesses or
        when the round is already finished.
        """
        if self.is_over():
            raise RuntimeError("this round is already over")
        if not self.is_valid_guess(guess):
            raise ValueError(
                f"guess must contain {self.code_length} colors numbered 1-{self.palette_size}"
            )
        exact = 0
        secret_rest = []
        guess_rest = []
        for guessed, actual in zip(guess, self.secret):
            if guessed == actual:
                exact += 1
            else:
                secret_rest.append(actual)
                guess_rest.append(guessed)
        available = Counter(secret_rest)
        partial = 0
        for guessed in guess_rest:
            if available[guessed] > 0:
                partial += 1
                available[guessed] -= 1
        self.attempts_used += 1
        if exact == self.code_length:
            self.solved = True
        return exact, partial
    def is_over(self):
        """True when the code is cracked or the attempt budget is spent."""
        return self.solved or self.attempts_used >= self.max_attempts
    def attempts_remaining(self):
        return self.max_attempts - self.attempts_used
    def is_win(self):
        return self.solved