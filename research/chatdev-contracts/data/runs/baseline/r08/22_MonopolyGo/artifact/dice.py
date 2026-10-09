'''
dice.py
A pair of six-sided dice with injectable randomness (rng) so the
game can be tested deterministically. roll() returns both the values
and whether the roll was doubles.
'''
import random
class Dice:
    """Two six-sided dice."""
    def __init__(self, sides=6, rng=None):
        self.sides = sides
        self.rng = rng if rng is not None else random.Random()
    def roll(self):
        """Roll both dice; returns (die1, die2, is_doubles)."""
        d1 = self.rng.randint(1, self.sides)
        d2 = self.rng.randint(1, self.sides)
        return d1, d2, d1 == d2