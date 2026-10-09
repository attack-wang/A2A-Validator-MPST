'''
Secret code generation module for the Mastermind game.
Randomly selects the hidden sequence of colors that the player must
crack. Supports both the classic variant (duplicate colors allowed)
and a harder variant where every color in the code is unique.
'''
import random
class CodeGenerator:
    '''Generates random secret codes from a given color palette.'''
    def __init__(self, rng=None):
        '''
        :param rng: optional random source exposing .choice/.sample
                    (defaults to the `random` module; injectable for tests)
        '''
        self.rng = rng if rng is not None else random
    def generate(self, colors, length, allow_duplicates=True):
        '''
        Generate a secret code as a list of color letters.
        :param colors: iterable of valid color letters
        :param length: desired secret code length
        :param allow_duplicates: if False, each color appears at most once
        :return: list of color letters representing the secret code
        :raises ValueError: if a unique code is requested but the palette
                            is too small to build one
        '''
        palette = list(colors)
        if not palette:
            raise ValueError("Color palette must not be empty.")
        if length <= 0:
            raise ValueError("Code length must be a positive integer.")
        if allow_duplicates:
            return [self.rng.choice(palette) for _ in range(length)]
        if length > len(palette):
            raise ValueError(
                f"Cannot build a code of length {length} without duplicates "
                f"from a palette of only {len(palette)} colors."
            )
        return self.rng.sample(palette, length)