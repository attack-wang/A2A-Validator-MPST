'''
entities.py
Entity classes: Player, Monster, TreasureChest.
'''
import random
import config
class Player:
    """The player character: grid position and hit points."""
    def __init__(self, x, y, hp=None):
        self.x = x
        self.y = y
        self.hp = hp if hp is not None else config.PLAYER_START_HP
        self.max_hp = config.PLAYER_MAX_HP
    def move_to(self, x, y):
        """Move the player to the given grid coordinates."""
        self.x = x
        self.y = y
    def heal(self, amount):
        """Restore HP up to max_hp; return the amount actually healed."""
        healed = min(self.max_hp, self.hp + amount) - self.hp
        self.hp += healed
        return healed
    def take_damage(self, amount):
        """Subtract damage from HP; return the resulting HP."""
        self.hp -= amount
        return self.hp
    def is_alive(self):
        """True while the player still has positive HP."""
        return self.hp > 0
class Monster:
    """A monster guarding the tower. Combat deals its HP as damage."""
    def __init__(self, x, y, name, hp):
        self.x = x
        self.y = y
        self.name = name
        self.hp = hp
    @property
    def damage(self):
        """Damage dealt to the player equals the monster's HP."""
        return self.hp
class TreasureChest:
    """A treasure chest that restores 20-30 HP when touched."""
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.heal_amount = random.randint(config.CHEST_HEAL_MIN,
                                          config.CHEST_HEAL_MAX)