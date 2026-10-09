"""
code_generator.py
Creation of the secret code the player must break.
- generate_secret_code(palette, code_length, allow_duplicates=True, rng=None):
  returns a list of palette labels. When duplicates are allowed every slot is
  drawn independently (symbols may repeat); otherwise the code is a random
  sample without repetition.
"""
import random
def generate_secret_code(palette, code_length, allow_duplicates=True, rng=None):
    """Build the hidden code as a list of palette labels."""
    if code_length < 1:
        raise ValueError("code_length must be at least 1")
    if code_length > len(palette) and not allow_duplicates:
        raise ValueError("cannot build a duplicate-free code longer than the palette")
    chooser = rng if rng is not None else random.Random()
    labels = [entry["label"] for entry in palette]
    if allow_duplicates:
        return [chooser.choice(labels) for _ in range(code_length)]
    return chooser.sample(labels, code_length)