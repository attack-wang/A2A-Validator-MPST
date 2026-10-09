'''
Configuration module for the Mastermind game.
Centralizes every tunable game setting in a single GameConfig dataclass:
the color palette (letter code -> display name), the secret code length,
the maximum number of attempts, and whether the secret code may contain
repeated colors. A "classic" preset implements the traditional Mastermind
rules (6 colors, code length 4, 10 attempts, duplicates allowed).
'''
from dataclasses import dataclass, field
@dataclass
class GameConfig:
    '''Container for all settings that control a Mastermind session.'''
    colors: dict = field(default_factory=dict)
    code_length: int = 4
    max_attempts: int = 10
    allow_duplicates: bool = True
    @property
    def color_letters(self):
        '''Return the list of valid single-letter color codes.'''
        return list(self.colors.keys())
    @property
    def valid_letters_str(self):
        '''Return a human-readable string of valid color letters.'''
        return " ".join(sorted(self.colors.keys()))
    @classmethod
    def classic(cls):
        '''Return the classic Mastermind configuration.'''
        return cls(
            colors={
                'R': 'Red',
                'G': 'Green',
                'B': 'Blue',
                'Y': 'Yellow',
                'O': 'Orange',
                'P': 'Purple',
            },
            code_length=4,
            max_attempts=10,
            allow_duplicates=True,
        )