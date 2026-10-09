'''
entities.py
Entity data classes: Player, Monster, TreasureChest, Door.
'''
class Player:
    """The player character: grid position and hit points."""
    def __init__(self, x, y, hp):
        self.x = x
        self.y = y
        self.hp = hp
        self.max_hp = hp
    @property
    def position(self):
        return (self.x, self.y)
    def is_alive(self):
        return self.hp > 0
class Monster:
    """An enemy occupying one floor tile; stepping on it triggers combat."""
    def __init__(self, x, y, name, hp, color):
        self.x = x
        self.y = y
        self.name = name
        self.hp = hp
        self.color = color
    @property
    def position(self):
        return (self.x, self.y)
class TreasureChest:
    """A pickup that restores 20-30 HP when stepped on."""
    def __init__(self, x, y, heal_amount):
        self.x = x
        self.y = y
        self.heal_amount = heal_amount
    @property
    def position(self):
        return (self.x, self.y)
class Door:
    """Exit tile; stepping on it advances to the next level."""
    def __init__(self, x, y):
        self.x = x
        self.y = y
    @property
    def position(self):
        return (self.x, self.y)