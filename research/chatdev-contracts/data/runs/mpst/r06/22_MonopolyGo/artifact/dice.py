'''
dice.py
Dice module for the simplified Monopoly Go! game.
Provides the Dice class which simulates rolling two six-sided dice,
detecting doubles, and producing human-readable descriptions of rolls.
'''
import random
class Dice:
    """Simulates a pair of six-sided dice used for movement and jail rolls."""
    def __init__(self, sides: int = 6):
        self.sides = sides
        self.last_roll = (0, 0)
    def roll(self):
        """Roll two dice. Returns (die1, die2)."""
        die1 = random.randint(1, self.sides)
        die2 = random.randint(1, self.sides)
        self.last_roll = (die1, die2)
        return self.last_roll
    def is_doubles(self, roll=None):
        """Return True if the given (or last) roll is doubles."""
        roll = roll if roll is not None else self.last_roll
        return roll[0] == roll[1]
    def total(self, roll=None):
        """Return the sum of the given (or last) roll."""
        roll = roll if roll is not None else self.last_roll
        return roll[0] + roll[1]
    @staticmethod
    def describe(roll):
        """Return a readable description such as 'rolled 4 + 3 = 7'."""
        die1, die2 = roll
        doubles = " (DOUBLES!)" if die1 == die2 else ""
        return f"rolled {die1} + {die2} = {die1 + die2}{doubles}"