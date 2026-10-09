'''
entities.py
Simple entity value objects: the Player, Monsters and Treasure Chests
that populate each floor of the tower.
'''
import random
from settings import CHEST_HEAL_MIN, CHEST_HEAL_MAX
class Player:
    '''The hero. Holds the grid position and the current hit points.'''
    def __init__(self, x, y, hp):
        self.x = x
        self.y = y
        self.hp = hp
    @property
    def pos(self):
        return (self.x, self.y)
class Monster:
    '''
    A tower monster. When the player steps onto its tile the monster's
    full HP is subtracted from the player's HP and the monster is slain.
    '''
    def __init__(self, name, hp, x, y):
        self.name = name
        self.hp = hp
        self.x = x
        self.y = y
    @property
    def pos(self):
        return (self.x, self.y)
class TreasureChest:
    '''
    A treasure chest. Touching it restores a random amount of HP
    between CHEST_HEAL_MIN and CHEST_HEAL_MAX (inclusive).
    '''
    def __init__(self, x, y, rng=random):
        self.x = x
        self.y = y
        self.heal = rng.randint(CHEST_HEAL_MIN, CHEST_HEAL_MAX)
    @property
    def pos(self):
        return (self.x, self.y)