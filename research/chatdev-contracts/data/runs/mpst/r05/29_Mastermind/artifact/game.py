'''
game.py
Core game engine for Mastermind.
MastermindGame stores the secret code, accepts validated guesses, computes
feedback for each attempt, and tracks whether the player has won (code
cracked) or lost (attempts exhausted).
'''
from feedback import evaluate_guess
class MastermindGame:
    """One round of Mastermind from secret generation to win/lose outcome."""
    def __init__(self, palette, code_length, max_attempts, secret=None):
        """
        Create a round. If `secret` is omitted a random one is drawn from
        `palette`; passing an explicit secret is useful for testing.
        """
        if code_length <= 0:
            raise ValueError('code_length must be positive.')
        if max_attempts <= 0:
            raise ValueError('max_attempts must be positive.')
        self.palette = palette
        self.code_length = code_length
        self.max_attempts = max_attempts
        self._secret = list(secret) if secret is not None else palette.random_secret(code_length)
        if len(self._secret) != code_length:
            raise ValueError('Provided secret does not match code_length.')
        self.guess_history = []     # list of guessed codes (lists of symbols)
        self.feedback_history = []  # list of Feedback objects, aligned with guesses
        self._is_over = False
        self._is_won = False
    # -- state ---------------------------------------------------------------
    @property
    def secret(self):
        """A copy of the secret code (safe to expose without mutation)."""
        return list(self._secret)
    @property
    def attempts_used(self):
        return len(self.guess_history)
    @property
    def attempts_remaining(self):
        return self.max_attempts - self.attempts_used
    @property
    def is_over(self):
        """True once the code is cracked or attempts are exhausted."""
        return self._is_over
    @property
    def is_won(self):
        return self._is_won
    @property
    def is_lost(self):
        return self._is_over and not self._is_won
    # -- gameplay --------------------------------------------------------------
    def is_valid_guess(self, symbols):
        """True if `symbols` is a well-formed guess for this round."""
        return (
            self.palette.is_valid_guess(symbols)
            and len(symbols) == self.code_length
        )
    def make_guess(self, symbols):
        """
        Submit a guess (list of color symbols).
        Returns the Feedback for this attempt and advances the game state.
        Raises ValueError for malformed guesses and RuntimeError if the
        round is already finished.
        """
        if self._is_over:
            raise RuntimeError('This round is already over.')
        if not self.is_valid_guess(symbols):
            raise ValueError(
                'Guess must be exactly {} colors from: {}'.format(
                    self.code_length, ' '.join(self.palette.symbols)
                )
            )
        feedback = evaluate_guess(self._secret, symbols)
        self.guess_history.append(list(symbols))
        self.feedback_history.append(feedback)
        if feedback.is_solved(self.code_length):
            self._is_over = True
            self._is_won = True
        elif self.attempts_used >= self.max_attempts:
            self._is_over = True
        return feedback