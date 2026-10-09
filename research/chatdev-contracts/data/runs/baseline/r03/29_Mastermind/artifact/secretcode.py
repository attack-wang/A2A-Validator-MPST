# secret_code.py
"""Random secret code generation."""
import random
class SecretCode:
    def __init__(self, palette, code_length, allow_duplicates=True, rng=None):
        self.palette = list(palette)
        self.code_length = code_length
        self.allow_duplicates = allow_duplicates
        self._rng = rng or random.Random()
        self._code = self._generate()
    def _generate(self):
        if self.allow_duplicates:
            return [self._rng.choice(self.palette) for _ in range(self.code_length)]
        return self._rng.sample(self.palette, self.code_length)
    @property
    def code(self):
        return list(self._code)  # return a copy to prevent mutation
    def reveal(self):
        return " ".join(self._code)