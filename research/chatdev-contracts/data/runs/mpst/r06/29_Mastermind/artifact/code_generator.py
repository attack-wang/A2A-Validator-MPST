'''
code_generator.py
Generation of the hidden secret code for the Mastermind game.
`SecretCodeGenerator` builds a random code of a given length from a set
of symbols. It supports both codes with duplicate symbols (classic
Mastermind rules) and codes where every symbol is unique.
'''
import random
class SecretCodeGenerator:
    """Creates the random secret code the player must crack."""
    def __init__(self, symbols, code_length, allow_duplicates=True, rng=None):
        if not symbols:
            raise ValueError("At least one symbol is required.")
        if code_length < 1:
            raise ValueError("code_length must be at least 1.")
        if not allow_duplicates and code_length > len(symbols):
            raise ValueError(
                "Unique-symbol codes cannot be longer than the symbol set."
            )
        self.symbols = list(symbols)
        self.code_length = code_length
        self.allow_duplicates = allow_duplicates
        self.rng = rng if rng is not None else random.Random()
    def generate(self):
        """Return a new random secret code as a list of symbols."""
        if self.allow_duplicates:
            return [self.rng.choice(self.symbols) for _ in range(self.code_length)]
        return self.rng.sample(self.symbols, self.code_length)