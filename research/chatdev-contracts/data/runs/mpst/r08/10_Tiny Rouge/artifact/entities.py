'''
entities.py
Entity classes: Player, Monster and TreasureChest.
'''
import random
import settings
class Player:
    """The player-controlled character: grid position and hit points."""
    def __init__(self, x, y, hp=settings.PLAYER_START_HP):
        self.x = x
        self.y = y
        self.hp = hp
        self.max_hp = max(hp, settings.PLAYER_START_HP)
    def heal(self, amount):
        """Restore HP, capped at max_hp. Returns the amount actually healed."""
        actual = min(amount, self.max_hp - self.hp)
        self.hp += actual
        return actual
    def take_damage(self, amount):
        """Apply damage and return the resulting HP (may be <= 0)."""
        self.hp -= amount
        return self.hp
    @property
    def is_dead(self):
        return self.hp <= 0
class Monster:
    """A hostile creature occupying one grid tile."""
    def __init__(self, x, y, definition, level):
        self.name = definition["name"]
        self.base_hp = definition["hp"]
        self.hp = max(1, int(round(definition["hp"] * (1 + settings.MONSTER_HP_LEVEL_SCALE * (level - 1)))))
        self.glyph = definition["glyph"]
        self.color = definition["color"]
        self.x = x
        self.y = y
class TreasureChest:
    """A chest that restores 20-30 HP when the player steps on it."""
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.heal_amount = random.randint(settings.CHEST_HEAL_MIN, settings.CHEST_HEAL_MAX)
        self.opened = False