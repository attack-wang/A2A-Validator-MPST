'''
dice.py
Provides a pair of six-sided dice used for movement,
doubles detection and jail escapes.
'''
import random
class Dice:
    """A pair of six-sided dice."""
    SIDES = 6
    def roll(self):
        """Roll both dice and return the individual results as a tuple."""
        die1 = random.randint(1, self.SIDES)
        die2 = random.randint(1, self.SIDES)
        return die1, die2
    @staticmethod
    def is_doubles(die1, die2):
        """Return True when both dice show the same face."""
        return die1 == die2