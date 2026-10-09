'''
game.py
Core game engine: secret generation, guess submission and win/lose state.
The engine is deliberately free of any I/O so it can be unit-tested.
'''
import random
from config import GameConfig
from feedback import compute_feedback
class GameEngine:
    '''Stateful Mastermind engine that owns the secret and the history.'''
    def __init__(self, config: GameConfig, rng=None):
        self.config = config
        self._rng = rng if rng is not None else random
        self._secret = []
        self._history = []
        self._tries_used = 0
        self._won = False
    def start(self):
        '''Begin (or restart) a game: reset all state and pick a fresh secret.'''
        self._secret = self.config.random_secret(self._rng)
        self._history = []
        self._tries_used = 0
        self._won = False
    def submit_guess(self, guess):
        '''Record one guess, update the state, and return its Feedback.'''
        if self.is_finished:
            raise RuntimeError('The game is already over; call start() to play again.')
        feedback = compute_feedback(guess, self._secret)
        self._history.append((list(guess), feedback))
        self._tries_used += 1
        if feedback.is_win(self.config.code_length):
            self._won = True
        return feedback
    @property
    def is_finished(self):
        '''True when the code is cracked or the tries are exhausted.'''
        return self._won or self._tries_used >= self.config.max_tries
    @property
    def is_won(self):
        '''True when the player cracked the code.'''
        return self._won
    @property
    def tries_used(self):
        '''Number of guesses submitted so far.'''
        return self._tries_used
    @property
    def tries_left(self):
        '''Number of guesses the player still has.'''
        return self.config.max_tries - self._tries_used
    @property
    def secret(self):
        '''A copy of the hidden sequence (revealed only at game end).'''
        return list(self._secret)
    @property
    def history(self):
        '''A copy of the (guess, feedback) pairs submitted so far.'''
        return list(self._history)