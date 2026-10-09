from settings import PLAYER_START_HP
class Player:
    def __init__(self, x, y, max_hp=PLAYER_START_HP):
        self.x = x
        self.y = y
        self.max_hp = max_hp
        self.hp = max_hp
    @property
    def pos(self):
        return (self.x, self.y)
    def heal(self, amount):
        before = self.hp
        self.hp = min(self.max_hp, self.hp + amount)
        return self.hp - before
    def take_damage(self, amount):
        self.hp -= amount
        return self.hp <= 0
MONSTER_TIERS = (
    ("Slime", 1.0),
    ("Red Slime", 1.25),
    ("Bat", 1.5),
    ("Skeleton", 1.9),
    ("Ghost", 2.4),
    ("Wizard", 3.0),
    ("Demon", 3.8),
)
class Monster:
    def __init__(self, x, y, name, hp):
        self.x = x; self.y = y; self.name = name; self.hp = hp
    @property
    def pos(self): return (self.x, self.y)
    @classmethod
    def spawn(cls, x, y, level, rng=random):
        # stronger tiers unlock as level rises
        max_tier = min(len(MONSTER_TIERS), 2 + level)  # level1 → 3 tiers
        tier_index = rng.randint(0, max_tier - 1)
        name, mult = MONSTER_TIERS[tier_index]
        base = rng.randint(6, 12)
        hp = max(1, int(round(base * mult * (1.0 + 0.22 * (level - 1)))))
        return cls(x, y, name, hp)
class Chest:
    def __init__(self, x, y, heal):
        self.x = x; self.y = y; self.heal = heal
    @property
    def pos(self): return (self.x, self.y)
    @classmethod
    def spawn(cls, x, y, rng=random):
        return cls(x, y, rng.randint(CHEST_HEAL_MIN, CHEST_HEAL_MAX))