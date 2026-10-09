class Monster:
    def __init__(self, x, y, definition, level):
        self.name = definition["name"]
        self.base_hp = definition["hp"]
        self.hp = max(1, int(round(definition["hp"] * (1 + settings.MONSTER_HP_LEVEL_SCALE * (level - 1)))))
        self.glyph = definition["glyph"]
        self.color = definition["color"]
        self.x = x
        self.y = y