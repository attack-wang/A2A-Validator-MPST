'''Entity classes: the player, monsters and treasure chests.'''
import random
import settings
class Player:
    '''The hero that explores the tower. Tracks position and hit points.'''
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.hp = settings.PLAYER_START_HP
    @property
    def pos(self):
        return (self.x, self.y)
    def is_alive(self):
        return self.hp > 0
    def take_damage(self, amount):
        self.hp -= amount
    def heal(self, amount):
        self.hp += amount
class Monster:
    '''A monster guarding a tile. Combat costs the player HP equal to monster HP.'''
    def __init__(self, name, hp, atk, color):
        self.name = name
        self.hp = hp
        self.atk = atk
        self.color = color
    @classmethod
    def spawn(cls, level, kind=None):
        '''Create a random monster scaled for the given tower level.
        The boss is excluded from the random pool; it is placed explicitly
        on the final floor by the map generator.'''
        if kind is None:
            kind = random.choice(settings.MONSTER_TYPES[:-1])
        scale = 1.0 + 0.15 * (level - 1)
        return cls(kind["name"], max(1, round(kind["hp"] * scale)),
                   kind["atk"], kind["color"])
    def __repr__(self):
        return f"Monster({self.name}, HP={self.hp}, ATK={self.atk})"
class TreasureChest:
    '''A chest that restores 20-30 HP when the player steps onto it.'''
    def __init__(self, heal_amount=None):
        self.heal_amount = (heal_amount if heal_amount is not None
                            else random.randint(settings.CHEST_HEAL_MIN,
                                                settings.CHEST_HEAL_MAX))