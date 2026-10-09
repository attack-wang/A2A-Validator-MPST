"""Dice rolling utilities for Monopoly Go!"""
import random
class Dice:
    """A pair of six-sided dice."""
    def __init__(self, sides=6, rng=None):
        self.sides = sides
        self.rng = rng or random
        self.last_roll = (0, 0)
    def roll(self):
        d1 = self.rng.randint(1, self.sides)
        d2 = self.rng.randint(1, self.sides)
        self.last_roll = (d1, d2)
        return self.last_roll
    @property
    def total(self):
        return sum(self.last_roll)
    @property
    def is_doubles(self):
        return self.last_roll[0] == self.last_roll[1] and self.last_roll != (0, 0)