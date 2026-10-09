class Gold(GameObject):
    SIZES = {
        "gold_small": (14, 50, 1.0),
        "gold_medium": (21, 150, 1.6),
        "gold_large": (30, 500, 2.6),
    }
    def __init__(self, kind, x, y):
        radius, value, weight = self.SIZES[kind]
        super().__init__(kind, x, y, radius, value, weight)
    def draw(self, surface):
        # nugget: irregular polygon based on seed