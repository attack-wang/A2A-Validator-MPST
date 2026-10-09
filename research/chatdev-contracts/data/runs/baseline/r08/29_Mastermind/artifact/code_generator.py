'''
code_generator.py
Creates the secret code that the player must crack.
The secret code is a sequence of color keys (see constants.COLORS).
Depending on the chosen difficulty, colors may or may not repeat
within the code.
'''
import random
from constants import COLORS
def generate_secret_code(code_length, color_count, allow_duplicates=True, rng=None):
    '''
    Generate a random secret code.
    Args:
        code_length: Number of pegs in the code.
        color_count: How many of the palette colors may be used
                     (the first N colors of the palette).
        allow_duplicates: Whether the same color may appear more than once.
        rng: Optional random source (defaults to the random module);
             injectable for deterministic tests.
    Returns:
        A list of color keys, e.g. ["3", "1", "3", "6"].
    '''
    rng = rng if rng is not None else random
    palette = list(COLORS.keys())[:color_count]
    if allow_duplicates:
        return [rng.choice(palette) for _ in range(code_length)]
    return rng.sample(palette, code_length)