'''
entities.py
Entity classes: Player, Monster and Treasure.
'''
import random
import settings
class Player:
    """The hero controlled with W/A/S/D. Tracks position and HP."""
    def __init__(self, x, y):
        """Create the player at (x, y) with the configured starting HP."""
        self.x = x
        self.y = y
        self.hp = settings.PLAYER_START_HP
    @property
    def pos(self):
        """Current grid position as a tuple."""
        return (self.x, self.y)
    def heal(self, amount):
        """Restore HP by the given amount."""
        self.hp += amount
    def damage(self, amount):
        """Subtract the given amount of HP."""
        self.hp -= amount
    @property
    def alive(self):
        """True while the player still has HP above zero."""
        return self.hp > 0
class Monster:
    """A stationary guardian. Combat costs the player HP equal to monster HP."""
    def __init__(self, x, y, name, hp, color):
        """Create a monster at (x, y) with the given name, HP and display color."""
        self.x = x
        self.y = y
        self.name = name
        self.hp = hp
        self.max_hp = hp
        self.color = color
    @property
    def pos(self):
        """Current grid position as a tuple."""
        return (self.x, self.y)
class Treasure:
    """A chest that restores 20-30 HP when stepped on."""
    def __init__(self, x, y):
        """Create a chest at (x, y) with a random heal amount in the configured range."""
        self.x = x
        self.y = y
        self.amount = random.randint(settings.TREASURE_MIN_HEAL,
                                     settings.TREASURE_MAX_HEAL)
    @property
    def pos(self):
        """Current grid position as a tuple."""
        return (self.x, self.y)