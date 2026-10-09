'''
Dice module: provides the Dice class used to simulate rolling two six-sided dice.
'''
import random
class Dice:
    """Simulates a pair of six-sided dice and remembers the last roll."""
    def __init__(self, sides=6):
        """Store the number of sides per die and initialise the last roll."""
        self.sides = sides
        self.last_roll = (0, 0)
    @property
    def last_total(self):
        """Return the sum of the most recent roll."""
        return sum(self.last_roll)
    @property
    def is_double(self):
        """Return True when both dice of the last roll show the same face."""
        return self.last_roll[0] == self.last_roll[1]
    def roll(self):
        """Roll both dice, store and return the result as a tuple."""
        self.last_roll = (random.randint(1, self.sides), random.randint(1, self.sides))
        return self.last_roll