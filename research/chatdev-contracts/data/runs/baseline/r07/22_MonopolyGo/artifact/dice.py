'''
dice.py
Dice rolling mechanics for the simplified Monopoly Go! game.
The Dice class models a pair of six-sided dice and reports whether the
roll was doubles, which is used for extra turns and jail escapes.
'''
import random
class Dice:
    """A pair of six-sided dice used to move players around the board."""
    def __init__(self):
        self.die1 = 0
        self.die2 = 0
    @property
    def total(self):
        """Sum of the two dice from the most recent roll."""
        return self.die1 + self.die2
    @property
    def is_doubles(self):
        """True when both dice show the same face on the most recent roll."""
        return self.die1 == self.die2
    def roll(self):
        """Roll both dice and return the total."""
        self.die1 = random.randint(1, 6)
        self.die2 = random.randint(1, 6)
        return self.total