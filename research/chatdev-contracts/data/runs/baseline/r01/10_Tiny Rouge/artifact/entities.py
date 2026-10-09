'''
Entity classes: Player, Monster, and Chest.
'''
import random
class Player:
    """The player character: position, HP, and movement state."""
    def __init__(self, x, y, max_hp=100, hp=100):
        self.x = x
        self.y = y
        self.max_hp = max_hp
        self.hp = hp
    def heal(self, amount):
        """Restore HP, capped at max_hp. Returns the actual amount healed."""
        actual = min(self.max_hp - self.hp, max(0, amount))
        self.hp += actual
        return actual
    def take_damage(self, amount):
        """Apply damage; HP is clamped at 0 minimum. Returns actual damage taken."""
        actual = max(0, amount)
        self.hp = max(0, self.hp - actual)
        return actual
    @property
    def is_alive(self):
        """True while HP is above zero."""
        return self.hp > 0
class Monster:
    """A monster occupying one grid tile; combat subtracts its HP from the player."""
    def __init__(self, x, y, name, hp, glyph, color):
        self.x = x
        self.y = y
        self.name = name
        self.hp = hp
        self.glyph = glyph
        self.color = color
class Chest:
    """A treasure chest; touching it restores 20-30 HP."""
    def __init__(self, x, y):
        self.x = x
        self.y = y