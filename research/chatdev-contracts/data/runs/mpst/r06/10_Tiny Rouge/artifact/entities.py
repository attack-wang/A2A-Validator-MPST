'''
entities.py
Data classes describing every object that can occupy a tile of the
80 x 80 grid: the player, monsters, treasure chests and the door that
leads to the next floor.
'''
import random
import game_constants as C
class Player:
    """The hero controlled with the W/A/S/D keys."""
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.max_hp = C.PLAYER_MAX_HP_BASE
        self.hp = C.PLAYER_START_HP
    @property
    def pos(self):
        return (self.x, self.y)
    def move_to(self, x, y):
        self.x = x
        self.y = y
    def take_damage(self, amount):
        self.hp = max(0, self.hp - amount)
    def heal(self, amount):
        self.hp = min(self.max_hp, self.hp + amount)
    def is_alive(self):
        return self.hp > 0
    def raise_max_hp(self, amount):
        self.max_hp += amount
class Monster:
    """A hostile creature; touching it costs the player HP equal to the monster's HP."""
    def __init__(self, x, y, name, hp, color):
        self.x = x
        self.y = y
        self.name = name
        self.hp = hp
        self.max_hp = hp
        self.color = color
    @property
    def pos(self):
        return (self.x, self.y)
    def stats_line(self):
        return f"{self.name}  HP {self.hp}/{self.max_hp}"
class TreasureChest:
    """A chest that restores a random 20-30 HP when stepped on."""
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.amount = random.randint(C.CHEST_HEAL_MIN, C.CHEST_HEAL_MAX)
    @property
    def pos(self):
        return (self.x, self.y)
class Door:
    """The exit of the current floor; stepping on it starts the next level."""
    def __init__(self, x, y):
        self.x = x
        self.y = y
    @property
    def pos(self):
        return (self.x, self.y)