'''
entities.py
Data classes for every interactive object on the grid:
Player, Monster, TreasureChest and Door.
Entities only hold state and tiny helpers; all game rules
(movement validation, combat, level flow) live in game.py.
'''
import random
from config import PLAYER_START_HP, PLAYER_MAX_HP, CHEST_HEAL_MIN, CHEST_HEAL_MAX
class Player:
    '''The hero controlled with W/A/S/D. Tracks position and HP.'''
    def __init__(self, x, y, hp=PLAYER_START_HP, max_hp=PLAYER_MAX_HP):
        self.x = x
        self.y = y
        self.hp = hp
        self.max_hp = max_hp
    @property
    def pos(self):
        return (self.x, self.y)
    def move_to(self, x, y):
        '''Teleport/step the player to a new grid position.'''
        self.x = x
        self.y = y
    def heal(self, amount):
        '''Restore HP, capped at max_hp. Returns the HP actually gained.'''
        actual = min(amount, self.max_hp - self.hp)
        if actual > 0:
            self.hp += actual
        return max(0, actual)
    def take_damage(self, amount):
        '''Lose HP (never below 0). Returns the damage actually applied.'''
        actual = min(amount, self.hp)
        self.hp -= actual
        return actual
    def is_alive(self):
        return self.hp > 0
class Monster:
    '''A hostile creature. Bumping into it costs the player HP equal to monster HP.'''
    def __init__(self, x, y, name, hp, symbol="m"):
        self.x = x
        self.y = y
        self.name = name
        self.hp = hp
        self.symbol = symbol
    @property
    def pos(self):
        return (self.x, self.y)
    def describe(self):
        '''Human-readable stat line for the UI, e.g. "Skeleton (HP 24)".'''
        return "{} (HP {})".format(self.name, self.hp)
class TreasureChest:
    '''Heals the player 20-30 HP when stepped on, then disappears.'''
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.heal_amount = random.randint(CHEST_HEAL_MIN, CHEST_HEAL_MAX)
    @property
    def pos(self):
        return (self.x, self.y)
class Door:
    '''Level exit. Stepping on it advances to the next dungeon level.'''
    def __init__(self, x, y):
        self.x = x
        self.y = y
    @property
    def pos(self):
        return (self.x, self.y)