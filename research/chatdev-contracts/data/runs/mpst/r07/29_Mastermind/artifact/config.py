'''
config.py
Central configuration for the Mastermind game.
Holds every tunable parameter of the game in one place: the palette of
colors, the length of the secret code, the maximum number of attempts,
whether duplicate colors are allowed in the secret, and the symbols
used to render feedback pegs in the console.
Changing the defaults here instantly changes the difficulty of the
game without touching any other module.
'''
class GameConfig:
    '''
    Immutable-ish container for game settings.
    Attributes:
        colors: ordered list of single-character color tokens the
            player may guess (e.g. R=Red, G=Green, B=Blue, Y=Yellow,
            O=Orange, P=Purple).
        code_length: number of positions in the secret code.
        max_attempts: number of guesses the player gets.
        allow_duplicates: whether the secret may reuse a color.
        exact_peg: symbol shown for a right-color-right-position hit.
        partial_peg: symbol shown for a right-color-wrong-position hit.
        miss_peg: symbol shown for an unused feedback slot.
    '''
    def __init__(
        self,
        colors=None,
        code_length=4,
        max_attempts=10,
        allow_duplicates=True,
        exact_peg='*',
        partial_peg='o',
        miss_peg='-',
    ):
        if colors is None:
            colors = ['R', 'G', 'B', 'Y', 'O', 'P']
        self.colors = list(colors)
        self.code_length = code_length
        self.max_attempts = max_attempts
        self.allow_duplicates = allow_duplicates
        self.exact_peg = exact_peg
        self.partial_peg = partial_peg
        self.miss_peg = miss_peg
        self._validate()
    def _validate(self):
        '''Sanity-check the configuration and raise ValueError if broken.'''
        if not self.colors:
            raise ValueError('GameConfig needs at least one color.')
        if any((not isinstance(c, str)) or len(c) != 1 for c in self.colors):
            raise ValueError('Every color must be a single character token.')
        if len(set(c.upper() for c in self.colors)) != len(self.colors):
            raise ValueError('Color tokens must be unique (case-insensitive).')
        if self.code_length < 1:
            raise ValueError('code_length must be at least 1.')
        if not self.allow_duplicates and self.code_length > len(self.colors):
            raise ValueError(
                'code_length cannot exceed the palette size when '
                'duplicates are not allowed.'
            )
        if self.max_attempts < 1:
            raise ValueError('max_attempts must be at least 1.')
    @property
    def color_key(self):
        '''Human-readable legend of the palette, e.g. "R=Red, G=Green, ...".'''
        names = ['Red', 'Green', 'Blue', 'Yellow', 'Orange', 'Purple']
        parts = []
        for i, token in enumerate(self.colors):
            name = names[i] if i < len(names) else 'Color %d' % (i + 1)
            parts.append('%s=%s' % (token, name))
        return ', '.join(parts)