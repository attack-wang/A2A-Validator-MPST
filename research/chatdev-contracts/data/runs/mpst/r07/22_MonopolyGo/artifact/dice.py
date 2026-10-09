'''
dice.py
Simple pair of six-sided dice with roll() returning both values
and whether doubles were rolled.
'''
import random
class Dice:
    def __init__(self, sides=6):
        self.sides = sides
        self.last_roll = (0, 0)
    def roll(self):
        d1 = random.randint(1, self.sides)
        d2 = random.randint(1, self.sides)
        self.last_roll = (d1, d2)
        return d1, d2
    @staticmethod
    def is_doubles(d1, d2):
        return d1 == d2