'''Entity classes: Player, Monster, Chest.'''
import random
from settings import (PLAYER_START_HP, CHEST_HEAL_MIN, CHEST_HEAL_MAX,
                      MONSTER_TIERS)
class Player:
    '''The hero: tracks position and hit points.'''
    def __init__(self, x, y, max_hp=PLAYER_START_HP):
        self.x = x
        self.y = y
        self.max_hp = max_hp
        self.hp = max_hp
    @property
    def pos(self):
        return (self.x, self.y)
    def heal(self, amount):
        '''Heal up to max_hp; return the amount actually restored.'''
        before = self.hp
        self.hp = min(self.max_hp, self.hp + amount)
        return self.hp - before
    def take_damage(self, amount):
        '''Apply damage; return True if the player died.'''
        self.hp -= amount
        return self.hp <= 0
class Monster:
    '''A stationary enemy; bumping into it costs the player its HP.'''
    def __init__(self, x, y, name, hp):
        self.x = x
        self.y = y
        self.name = name
        self.hp = hp
    @property
    def pos(self):
        return (self.x, self.y)
    @classmethod
    def spawn(cls, x, y, level, rng=random):
        '''Create a monster whose strength scales with the tower level.'''
        max_tier = min(len(MONSTER_TIERS), 2 + level)  # level 1 -> 3 tiers
        tier_index = rng.randint(0, max_tier - 1)
        name, mult = MONSTER_TIERS[tier_index]
        base = rng.randint(6, 12)
        hp = max(1, int(round(base * mult * (1.0 + 0.22 * (level - 1)))))
        return cls(x, y, name, hp)
class Chest:
    '''A treasure chest that restores 20-30 HP when touched.'''
    def __init__(self, x, y, heal):
        self.x = x
        self.y = y
        self.heal = heal
    @property
    def pos(self):
        return (self.x, self.y)
    @classmethod
    def spawn(cls, x, y, rng=random):
        return cls(x, y, rng.randint(CHEST_HEAL_MIN, CHEST_HEAL_MAX))