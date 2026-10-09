'''Entity classes: Player, Monster, TreasureChest.'''
class Player:
    def __init__(self, x, y, hp=..., max_hp=...):
        self.x = x; self.y = y
        self.max_hp = max_hp
        self.hp = hp
    @property position...
    def heal(self, amount): self.hp = min(self.max_hp, self.hp + amount)
    def take_damage(self, dmg): self.hp -= dmg
class Monster:
    def __init__(self, x, y, name, hp, color, glyph):
        ...
class TreasureChest:
    def __init__(self, x, y, heal):
        ...