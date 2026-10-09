import random
class Dice:
    """A pair of six-sided dice used for movement and jail rolls."""
    def __init__(self, sides=6):
        self.sides = sides
    def roll(self):
        d1 = random.randint(1, self.sides)
        d2 = random.randint(1, self.sides)
        return d1, d2, d1 + d2, d1 == d2