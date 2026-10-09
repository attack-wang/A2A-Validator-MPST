'''
config.py
Game configuration for the Mastermind console game.
'''
import random
class GameConfig:
    '''Settings describing one Mastermind variant.'''
    DEFAULT_COLORS = ['R', 'G', 'B', 'Y', 'M', 'C']
    def __init__(self, code_length=4, colors=None, max_tries=10, seed=None):
        self.code_length = code_length
        self.colors = list(colors) if colors is not None else list(self.DEFAULT_COLORS)
        self.max_tries = max_tries
        self.seed = seed
    def validate(self):
        '''Raise ValueError when the settings cannot produce a fair game.'''
        if self.code_length < 1:
            raise ValueError('code_length must be at least 1.')
        if self.max_tries < 1:
            raise ValueError('max_tries must be at least 1.')
        if not self.colors:
            raise ValueError('colors must contain at least one color.')
        if len(set(self.colors)) != len(self.colors):
            raise ValueError('colors must not contain duplicates.')
        for color in self.colors:
            if (not isinstance(color, str) or len(color) != 1
                    or not color.isalpha() or not color.isupper()):
                raise ValueError(
                    f'Invalid color token {color!r}; use single uppercase letters.')
    def random_secret(self, rng=None):
        '''Return a random secret drawn (with repetition) from the palette.'''
        rng = rng if rng is not None else random
        return [rng.choice(self.colors) for _ in range(self.code_length)]