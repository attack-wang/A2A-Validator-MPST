class TreasureChest:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.heal_amount = random.randint(settings.CHEST_HEAL_MIN, settings.CHEST_HEAL_MAX)
        self.opened = False