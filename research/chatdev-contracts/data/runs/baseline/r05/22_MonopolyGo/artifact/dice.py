'''
dice.py
Dice module for the simplified Monopoly Go! game.
Provides the Dice class used to roll two six-sided dice and detect doubles.
'''
import random
class Dice:
    """A pair of six-sided dice used for movement and jail rolls."""
    def __init__(self, seed=None):
        """Initialise the dice with an optional fixed seed (useful for testing)."""
        self._rng = random.Random(seed)
        self.last_roll = (0, 0)
    def roll(self):
        """Roll both dice and return the tuple (die1, die2)."""
        self.last_roll = (self._rng.randint(1, 6), self._rng.randint(1, 6))
        return self.last_roll
    @property
    def last_total(self):
        """Total shown on the last roll."""
        return sum(self.last_roll)
    @property
    def last_is_doubles(self):
        """True when both dice of the last roll show the same value."""
        return self.last_roll[0] == self.last_roll[1]