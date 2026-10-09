'''
entities.py
Player and Monster entity classes for the Tower of the Sorcerer roguelike.
'''
class Player:
    """The player character: tracks HP and grid position."""
    def __init__(self, x, y, hp):
        self.x = x
        self.y = y
        self.hp = hp
        self.max_hp = hp  # grows if chests heal beyond the starting HP
    @property
    def position(self):
        return (self.x, self.y)
    def move_to(self, x, y):
        self.x = x
        self.y = y
    def take_damage(self, amount):
        self.hp -= amount
    def heal(self, amount):
        self.hp += amount
        if self.hp > self.max_hp:
            self.max_hp = self.hp
    def is_alive(self):
        return self.hp > 0
class Monster:
    """A monster occupying a grid tile; combat subtracts its HP from the player's."""
    def __init__(self, name, hp, color, x, y):
        self.name = name
        self.hp = hp
        self.color = color
        self.x = x
        self.y = y
    @property
    def position(self):
        return (self.x, self.y)