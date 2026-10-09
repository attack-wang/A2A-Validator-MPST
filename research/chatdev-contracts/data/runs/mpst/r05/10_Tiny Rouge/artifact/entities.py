"""Entity classes: Player, Monster, and TreasureChest."""
import random
import config
class Player:
    """The player character: grid position and hit points."""
    def __init__(self, x, y, hp=config.PLAYER_START_HP):
        self.x = x
        self.y = y
        self.hp = hp
    @property
    def position(self):
        return (self.x, self.y)
    @property
    def is_alive(self):
        return self.hp > 0
    def take_damage(self, amount):
        """Subtract damage from HP (combat: monster HP is the damage)."""
        self.hp -= amount
        return self.hp
    def heal(self, amount):
        """Restore HP by the given amount."""
        self.hp += amount
        return self.hp
class Monster:
    """A monster standing on a floor tile.
    Combat rule (per design): when the player bumps into a monster,
    the monster's HP is subtracted from the player's HP and the monster
    is defeated. Its HP is therefore also its contact damage.
    """
    NAMES = ["Slime", "Bat", "Skeleton", "Zombie", "Ghost",
             "Golem", "Wraith", "Demon", "Sorcerer"]
    def __init__(self, x, y, hp, name=None):
        self.x = x
        self.y = y
        self.hp = max(1, hp)
        self.name = name if name else random.choice(self.NAMES)
    @property
    def position(self):
        return (self.x, self.y)
    def stats_text(self):
        return "{}  HP {}  (deals {} on contact)".format(self.name, self.hp, self.hp)
class TreasureChest:
    """A treasure chest that restores 20-30 HP when touched."""
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.heal_amount = random.randint(config.CHEST_HEAL_MIN, config.CHEST_HEAL_MAX)
    @property
    def position(self):
        return (self.x, self.y)