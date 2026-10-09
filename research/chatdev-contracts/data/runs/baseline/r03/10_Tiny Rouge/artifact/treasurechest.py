'''
treasurechest.py
Treasure chest entity. When the player touches a chest it restores a random
amount of HP between CHEST_HEAL_MIN (20) and CHEST_HEAL_MAX (30) and the
chest disappears from the map.
'''
import random
import config
class TreasureChest:
    '''A treasure chest that restores 20-30 HP when touched.'''
    def __init__(self, x, y):
        self.x = x
        self.y = y
    @property
    def pos(self):
        return (self.x, self.y)
    def open(self):
        return random.randint(config.CHEST_HEAL_MIN, config.CHEST_HEAL_MAX)