'''
Dice rolling utilities for the Monopoly Go! game.
'''
import random
class Dice:
    """A pair of six-sided dice used to move players around the board."""
    def __init__(self, sides=6, seed=None):
        self.sides = sides
        self._random = random.Random(seed)
    def roll(self):
        """Roll two dice and return (die1, die2, is_doubles)."""
        die1 = self._random.randint(1, self.sides)
        die2 = self._random.randint(1, self.sides)
        return die1, die2, die1 == die2