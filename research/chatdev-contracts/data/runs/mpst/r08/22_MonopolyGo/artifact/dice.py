'''
dice.py
Two six-sided dice used for movement and jail rolls.
'''
import random
class Dice:
    """Static helper that rolls two independent six-sided dice."""
    @staticmethod
    def roll():
        """Return a tuple with two dice results, each between 1 and 6."""
        d1 = random.randint(1, 6)
        d2 = random.randint(1, 6)
        return d1, d2