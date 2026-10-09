'''
dice.py — Dice rolling...
'''
import random
class Dice:
    """A pair of six-sided dice."""
    def __init__(self, sides=6):
        self.sides = sides
    def roll(self):
        """Roll two dice; returns (die1, die2, total, is_double)."""
        d1 = random.randint(1, self.sides)
        d2 = random.randint(1, self.sides)
        return d1, d2