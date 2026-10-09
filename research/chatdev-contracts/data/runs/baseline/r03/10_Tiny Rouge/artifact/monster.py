'''
monster.py
Monster entity for the roguelike game. A monster guards a floor tile and its
HP scales with the current dungeon level. Combat subtracts the monster's HP
from the player's HP; ATK / DEF are flavour statistics shown in the UI.
'''
import config
class Monster:
    '''A monster guarding the tower. Combat subtracts its HP from player HP.'''
    def __init__(self, x, y, archetype, level):
        self.x = x
        self.y = y
        self.name = archetype["name"]
        self.atk = archetype["atk"]
        self.defense = archetype["defense"]
        self.color = archetype["color"]
        scale = 1.0 + config.MONSTER_HP_SCALE_PER_LEVEL * (level - 1)
        self.hp = max(1, int(round(archetype["hp"] * scale)))
    @property
    def pos(self):
        return (self.x, self.y)
    def stats_text(self):
        return f"{self.name} (HP {self.hp}, ATK {self.atk}, DEF {self.defense})"