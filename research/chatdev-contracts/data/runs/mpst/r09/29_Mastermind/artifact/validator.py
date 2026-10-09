'''
validator.py
Parsing and validation of raw player input into a guess.
'''
from config import GameConfig
class InputValidator:
    '''Turns raw text such as "RGBY" into a validated guess list.'''
    def __init__(self, config: GameConfig):
        self._config = config
        self._allowed = set(config.colors)
    def parse(self, raw):
        '''Return (guess, error): guess is a list of color letters on
        success (error is None); otherwise guess is None and error
        describes the problem for the player.
        '''
        text = (raw or '').strip().upper().replace(' ', '')
        if not text:
            return None, 'Empty input — please enter a guess like "RGBY".'
        guess = list(text)
        if len(guess) != self._config.code_length:
            return None, (f'Guess must be exactly {self._config.code_length} '
                          f'colors, got {len(guess)}.')
        for letter in guess:
            if letter not in self._allowed:
                allowed = ''.join(self._config.colors)
                return None, f'Invalid color "{letter}". Allowed colors: {allowed}.'
        return guess, None