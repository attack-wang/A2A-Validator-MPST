'''
dice.py
Defines the Dice class used by the game to simulate rolling a pair of
six-sided dice. Each roll returns both individual die values so the game
can detect doubles (used for extra turns and escaping jail).
'''
import random
class Dice:
    """A pair of six-sided dice."""
    def __init__(self, sides: int = 6, seed: int = None):
        self.sides = sides
        self._rng = random.Random(seed)
    def roll(self):
        """Roll both dice and return (die1, die2)."""
        return self._rng.randint(1, self.sides), self._rng.randint(1, self.sides)
    @staticmethod
    def is_double(roll):
        """Return True if both dice in `roll` show the same face."""
        return roll[0] == roll[1]