"""Entity data classes: the player and the monsters inhabiting the tower.
This module is the ONLY place where Monster is defined (the old duplicate
monster.py was removed to avoid import ambiguity).
"""
from dataclasses import dataclass
import settings
@dataclass
class Monster:
    """A monster guarding a floor tile.
    Touching it costs the player HP equal to the monster's HP; if the
    player survives, the monster is defeated and removed.
    """
    name: str
    hp: int
class Player:
    """The hero climbing the tower."""
    def __init__(self, row, col):
        self.row = row
        self.col = col
        self.max_hp = settings.PLAYER_START_MAX_HP
        self.hp = self.max_hp
    @property
    def position(self):
        """Current (row, col) position."""
        return (self.row, self.col)
    def heal(self, amount):
        """Restore HP up to max; return the amount actually healed."""
        before = self.hp
        self.hp = min(self.max_hp, self.hp + amount)
        return self.hp - before
    def take_damage(self, amount):
        """Subtract damage from HP; return True if the player survived."""
        self.hp -= amount
        return self.hp > 0
    def is_alive(self):
        return self.hp > 0