'''
dice.py
Module defining the Dice class used to simulate rolling a pair of
six-sided dice for the simplified Monopoly Go! game.
'''
import random
class Dice:
    '''A pair of six-sided dice with memory of the most recent roll.'''
    def __init__(self):
        '''Initialize the dice with no previous roll recorded.'''
        self.last_roll = (0, 0)
    def roll(self):
        '''
        Roll both dice.
        Returns:
            tuple: (die1, die2, total, is_doubles)
        '''
        die1 = random.randint(1, 6)
        die2 = random.randint(1, 6)
        self.last_roll = (die1, die2)
        return die1, die2, die1 + die2, (die1 == die2)