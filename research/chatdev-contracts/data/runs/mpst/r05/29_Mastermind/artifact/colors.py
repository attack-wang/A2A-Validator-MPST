'''
colors.py
Color palette handling for Mastermind.
Provides the set of symbols the secret code is built from, converts raw
player input into a normalized list of color symbols (accepting single
letters such as "RGBY" or full names such as "red, green, blue, yellow"),
and generates random secret codes.
'''
import random
import re
class ColorPalette:
    """The collection of colors available for codes and guesses."""
    def __init__(self, symbols, names):
        self._symbols = list(symbols)
        self._names = dict(names)
        # Case-insensitive lookup tables for input parsing.
        self._letter_lookup = {symbol.upper(): symbol for symbol in self._symbols}
        self._name_lookup = {name.upper(): symbol for symbol, name in self._names.items()}
    # -- basic accessors ----------------------------------------------------
    @property
    def symbols(self):
        """List of single-letter color symbols, e.g. ['R', 'G', ...]."""
        return list(self._symbols)
    @property
    def names(self):
        """Mapping from symbol to full color name, e.g. {'R': 'Red', ...}."""
        return dict(self._names)
    def name_of(self, symbol):
        """Full color name for a symbol, e.g. name_of('R') -> 'Red'."""
        return self._names.get(symbol, symbol)
    def __len__(self):
        return len(self._symbols)
    # -- input handling -----------------------------------------------------
    def normalize(self, raw_input):
        """
        Convert raw player input into a list of color symbols.
        Accepts single letters ("RGBY", "R G B Y", "r,g,b,y") and full
        color names ("red green blue yellow"). Returns the list of
        symbols, or None if any token is not a known color.
        """
        text = (raw_input or '').strip().lower()
        if not text:
            return None
        tokens = [token for token in re.split(r'[,\s]+', text) if token]
        # Allow a compact run of single letters such as "rgbY".
        if len(tokens) == 1 and len(tokens[0]) > 1:
            letters = list(tokens[0].upper())
            if all(letter in self._letter_lookup for letter in letters):
                tokens = letters
        symbols = []
        for token in tokens:
            symbol = self._match_token(token)
            if symbol is None:
                return None
            symbols.append(symbol)
        return symbols
    def _match_token(self, token):
        """Resolve one input token to a color symbol, or None if unknown."""
        candidate = token.upper()
        if candidate in self._letter_lookup:
            return self._letter_lookup[candidate]
        return self._name_lookup.get(candidate)
    def is_valid_guess(self, symbols):
        """True if `symbols` is a list of known colors of any length."""
        return (
            isinstance(symbols, list)
            and len(symbols) > 0
            and all(symbol in self._letter_lookup for symbol in symbols)
        )
    # -- secret generation ----------------------------------------------------
    def random_secret(self, length):
        """Generate a random secret code of the given length (repeats allowed)."""
        return [random.choice(self._symbols) for _ in range(length)]