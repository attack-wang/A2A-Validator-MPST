'''
dice.py
Dice rolling module for the simplified Monopoly Go! game.
'''
import random
class Dice:
    """A pair of six-sided dice used to move players around the board."""
    def __init__(self, sides=6, rng=None):
        self.sides = sides
        self.rng = rng or random
        self.last_roll = (0, 0)
    def roll(self):
        """Roll both dice, store and return the result as (die1, die2)."""
        die1 = self.rng.randint(1, self.sides)
        die2 = self.rng.randint(1, self.sides)
        self.last_roll = (die1, die2)
        return self.last_roll
    @property
    def total(self):
        return sum(self.last_roll)
    @property
    def is_doubles(self):
        return self.last_roll[0] == self.last_roll[1]