'''dice.py — Handles rolling two six-sided dice.'''
import random
class Dice:
    """Handles rolling two six-sided dice."""
    def __init__(self, sides=6, rng=None):
        self.sides = sides
        self.rng = rng or random.Random()
    def roll(self):
        """Roll two dice, return (die1, die2, total, is_doubles)."""
        d1 = self.rng.randint(1, self.sides)
        d2 = self.rng.randint(1, self.sides)
        return d1, d2, d1 + d2, d1 == d2