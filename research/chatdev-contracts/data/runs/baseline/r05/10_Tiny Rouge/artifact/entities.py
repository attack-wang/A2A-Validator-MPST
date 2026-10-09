'''
entities.py
Entity classes: the player character and the monsters inhabiting the tower.
Consolidated into a single module so that all game modules import from
one place (fixes the previous duplicate/broken import problem).
'''
import random
import config
class Player:
    '''Represents the player character: grid position and hit points.'''
    def __init__(self, x, y, hp=config.PLAYER_START_HP):
        '''Create a player at (x, y) with the given starting HP.'''
        self.x = x
        self.y = y
        self.hp = hp
    @property
    def position(self):
        '''Return the player's grid coordinates as an (x, y) tuple.'''
        return (self.x, self.y)
    def move_to(self, x, y):
        '''Teleport/move the player to the given grid coordinates.'''
        self.x = x
        self.y = y
    def take_damage(self, amount):
        '''Subtract damage from HP and return the new HP value.'''
        self.hp -= amount
        return self.hp
    def heal(self, amount):
        '''Add HP (from chests etc.) and return the new HP value.'''
        self.hp += amount
        return self.hp
    def is_dead(self):
        '''True when the player's HP has dropped to zero or below.'''
        return self.hp <= 0
class Monster:
    '''A monster guarding a tile. Its HP is the damage dealt to the player.'''
    def __init__(self, name, hp, x, y):
        '''Create a monster with a name, HP (=damage) and grid position.'''
        self.name = name
        self.hp = hp
        self.x = x
        self.y = y
    @classmethod
    def random(cls, x, y, level, rng=None):
        '''Build a random monster scaled by the current dungeon level.'''
        chooser = rng if rng is not None else random
        name, base = chooser.choice(config.MONSTER_TYPES)
        hp = base + (level - 1) * config.LEVEL_HP_SCALE
        return cls(name, hp, x, y)
    @property
    def position(self):
        '''Return the monster's grid coordinates as an (x, y) tuple.'''
        return (self.x, self.y)
    def describe(self):
        '''Human-readable stat line used by the UI panel.'''
        return f"{self.name} (HP {self.hp})"