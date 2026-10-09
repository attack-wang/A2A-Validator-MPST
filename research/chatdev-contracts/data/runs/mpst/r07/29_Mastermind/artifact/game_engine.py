'''
game_engine.py
Core game logic for the Mastermind game.
GameEngine owns the hidden secret code, tracks the number of used
attempts, stores the guess/feedback history, and decides when the
game is won or lost. It is completely independent from the console
UI so the same engine could drive any front end.
'''
import random
from feedback import compute_feedback
class GameOverError(Exception):
    '''Raised when a guess is submitted after the game has ended.'''
class GameEngine:
    '''
    State machine for a single Mastermind round.
    Lifecycle:
        engine = GameEngine(config)
        engine.start()               # rolls a new secret
        feedback = engine.submit_guess(['R', 'G', 'B', 'Y'])
        ...                          # repeat until win/lose
        engine.game_over -> True
    '''
    def __init__(self, config, rng=None):
        '''
        Args:
            config: GameConfig instance with palette/length/attempts.
            rng: optional random number generator (defaults to the
                global `random` module); injectable for testing.
        '''
        self.config = config
        self.rng = rng if rng is not None else random
        self.secret = []
        self.history = []  # list of (guess_list, Feedback) tuples
        self.finished = False
        self.won = False
    def start(self):
        '''Generate a fresh secret code and reset all round state.'''
        self.secret = self._generate_secret()
        self.history = []
        self.finished = False
        self.won = False
    def _generate_secret(self):
        '''
        Roll the hidden code.
        Uses `rng.choice` when duplicates are allowed and `rng.sample`
        (which never repeats) otherwise.
        '''
        if self.config.allow_duplicates:
            return [self.rng.choice(self.config.colors)
                    for _ in range(self.config.code_length)]
        return list(self.rng.sample(self.config.colors, self.config.code_length))
    @property
    def attempts_used(self):
        '''Number of guesses submitted so far.'''
        return len(self.history)
    @property
    def attempts_remaining(self):
        '''Guesses the player still has before losing.'''
        return self.config.max_attempts - self.attempts_used
    @property
    def game_over(self):
        '''True once the code is cracked or attempts are exhausted.'''
        return self.finished
    def submit_guess(self, guess):
        '''
        Process one guess.
        Args:
            guess: list of color tokens (already validated by
                validator.parse_guess).
        Returns:
            The Feedback for this guess.
        Raises:
            GameOverError: if the round has already ended.
            ValueError: if the guess length is wrong (defensive check;
                the validator normally guarantees correctness).
        '''
        if self.finished:
            raise GameOverError('This round is already over -- start a new game.')
        feedback = compute_feedback(guess, self.secret)
        self.history.append((list(guess), feedback))
        if feedback.is_win:
            self.finished = True
            self.won = True
        elif self.attempts_used >= self.config.max_attempts:
            self.finished = True
            self.won = False
        return feedback