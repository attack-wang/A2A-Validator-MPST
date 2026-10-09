"""Dice module: handles rolling two six-sided dice."""
import random
class Dice:
    """A pair of six-sided dice used for movement."""
    def __init__(self):
        self.last_roll = (0, 0)
    def roll(self):
        """Roll both dice. Returns (die1, die2, total, is_doubles)."""
        die1 = random.randint(1, 6)
        die2 = random.randint(1, 6)
        self.last_roll = (die1, die2)
        return die1, die2, die1 + die2, die1 == die2