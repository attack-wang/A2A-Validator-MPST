class Dice:
    def __init__(self, sides=6):
        self.sides = sides
    def roll(self):
        d1 = random.randint(1, self.sides)
        d2 = random.randint(1, self.sides)
        return d1, d2