class Player:
    def __init__(self, x, y, hp=config.PLAYER_START_HP):
        self.x = x
        self.y = y
        self.hp = hp
    def as_dict(self): ...  # not needed
class Monster:
    '''A monster guarding a tile. Its HP is the damage dealt to the player.'''
    def __init__(self, name, hp, x, y):
        self.name = name
        self.hp = hp
        self.x = x
        self.y = y
    @classmethod
    def random(cls, x, y, level):
        name, base = random.choice(config.MONSTER_TYPES)
        hp = base + (level - 1) * config.LEVEL_HP_SCALE
        return cls(name, hp, x, y)