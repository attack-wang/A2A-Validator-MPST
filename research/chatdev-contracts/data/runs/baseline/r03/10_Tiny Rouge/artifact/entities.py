'''
entities.py
Entity classes for the roguelike game: Player, Monster, TreasureChest and Door.
Every entity stores its grid coordinates. The Player tracks HP and provides
helpers for healing (capped at max HP) and taking damage. Monsters scale their
HP with the current dungeon level. TreasureChest rolls a random heal amount in
the configured 20-30 range. Door marks the level exit.
'''
import random
import config
class Player:
    '''The player character. Moves on floor tiles and fights monsters.'''
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.hp = config.PLAYER_START_HP
        self.max_hp = config.PLAYER_START_HP
    @property
    def pos(self):
        return (self.x, self.y)
    @property
    def alive(self):
        return self.hp > 0
    def move(self, dx, dy):
        self.x += dx
        self.y += dy
    def heal(self, amount):
        '''Restore HP, capped at max_hp.'''
        self.hp = min(self.hp + amount, self.max_hp)
    def take_damage(self, amount):
        '''Reduce HP, never below zero.'''
        self.hp = max(self.hp - amount, 0)