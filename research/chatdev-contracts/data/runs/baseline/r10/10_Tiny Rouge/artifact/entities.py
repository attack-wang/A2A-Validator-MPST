"""Entity classes: Player, Monster, and TreasureChest."""
class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.hp = PLAYER_START_HP
        self.max_hp = PLAYER_MAX_HP_BASE
    def heal(self, amount): ...
    def take_damage(self, amount): returns actual damage / sets hp
    @property is_alive