'''
entities.py
Entity classes for the game: Player, Monster and TreasureChest.
Instances are plain data holders; all game rules live in game.py.
'''
import config
class Player:
    """The player character: grid position + hit points."""
    def __init__(self, x, y, hp):
        self.x = x
        self.y = y
        self.hp = hp
        self.max_hp = config.PLAYER_MAX_HP
    @property
    def position(self):
        return (self.x, self.y)
    def move_to(self, x, y):
        self.x, self.y = x, y
    def is_alive(self):
        return self.hp > 0
    def heal(self, amount):
        """Restore HP, capped at max_hp. Returns the amount actually healed."""
        actual = min(amount, self.max_hp - self.hp)
        self.hp += max(0, actual)
        return max(0, actual)
    def take_damage(self, amount):
        """Subtract HP; clamped at 0 so it never goes negative."""
        self.hp = max(0, self.hp - amount)
class Monster:
    """A stationary monster. Its HP doubles as its attack: on contact the
    player loses exactly `hp` hit points and the monster is removed."""
    def __init__(self, x, y, hp, name):
        self.x = x
        self.y = y
        self.hp = hp
        self.name = name
        self.alive = True
    @property
    def position(self):
        return (self.x, self.y)
    def defeat(self):
        self.alive = False
class TreasureChest:
    """A treasure chest that restores a random 20-30 HP when touched."""
    def __init__(self, x, y, heal_amount):
        self.x = x
        self.y = y
        self.heal_amount = heal_amount
        self.opened = False
    @property
    def position(self):
        return (self.x, self.y)
    def open(self):
        self.opened = True
        return self.heal_amount