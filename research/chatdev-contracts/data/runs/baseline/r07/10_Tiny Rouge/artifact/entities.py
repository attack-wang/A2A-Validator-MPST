'''
entities.py
Entity data classes: Player, Monster, Chest, Door.
'''
import random
import settings
class Entity:
    '''Base class for anything that occupies a grid tile.'''
    def __init__(self, x, y):
        self.x = x
        self.y = y
    @property
    def pos(self):
        '''Current grid position as an (x, y) tuple.'''
        return (self.x, self.y)
    def __repr__(self):
        return f"{self.__class__.__name__}(x={self.x}, y={self.y})"
class Player(Entity):
    '''The player character: tracks grid position and hit points.'''
    def __init__(self, x, y, hp=settings.PLAYER_START_HP):
        super().__init__(x, y)
        self.hp = hp
        self.max_hp = hp
    def heal(self, amount):
        '''Restore HP (used by treasure chests, +20..30).'''
        self.hp += amount
        if self.hp > self.max_hp:
            self.max_hp = self.hp
        return self.hp
    def take_damage(self, amount):
        '''Subtract damage (a monster's HP) from the player's HP.
        Returns True when the hit reduces HP to zero or below (death).
        '''
        self.hp -= amount
        return self.hp <= 0
    @property
    def alive(self):
        '''The player is alive while HP is above zero.'''
        return self.hp > 0
class Monster(Entity):
    '''A monster guarding a tile. Combat subtracts its HP from the player's HP.'''
    def __init__(self, x, y, name, hp, color):
        super().__init__(x, y)
        self.name = name
        self.hp = hp
        self.color = color
    def __repr__(self):
        return f"Monster({self.name}, HP={self.hp}, pos={self.pos})"
class Chest(Entity):
    '''A treasure chest that restores 20-30 HP when touched.'''
    def __init__(self, x, y):
        super().__init__(x, y)
        self.heal_amount = random.randint(settings.CHEST_HEAL_MIN,
                                          settings.CHEST_HEAL_MAX)
class Door(Entity):
    '''The level exit. Reaching it advances the player to the next floor.'''
    pass