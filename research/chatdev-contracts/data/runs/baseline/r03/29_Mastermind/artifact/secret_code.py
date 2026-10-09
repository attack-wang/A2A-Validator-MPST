'''
secret_code.py
Generation and safe handling of the hidden secret code.
'''
import random
class SecretCode:
    """Generates and guards the hidden code the player must break."""
    def __init__(self, palette, code_length, allow_duplicates=True, rng=None):
        if code_length > len(palette) and not allow_duplicates:
            raise ValueError("Cannot build a duplicate-free code longer than the palette.")
        self._palette = list(palette)
        self._code_length = code_length
        self._allow_duplicates = allow_duplicates
        self._rng = rng if rng is not None else random.Random()
        self._code = self._generate()
    def _generate(self):
        """Roll a fresh random code according to the difficulty rules."""
        if self._allow_duplicates:
            return [self._rng.choice(self._palette) for _ in range(self._code_length)]
        return self._rng.sample(self._palette, self._code_length)
    @property
    def code(self):
        """A defensive copy of the secret (callers cannot mutate it)."""
        return list(self._code)
    @property
    def code_length(self):
        return self._code_length
    def reveal(self) -> str:
        """Human-readable reveal of the secret, used at game end."""
        return " ".join(self._code)