class Gold(GameObject):
    """Nuggets of gold in three sizes; heavier nuggets reel in slower."""
    SIZES = {
        'small': (18, GOLD_SMALL_VALUE, 1.0),
        'medium': (26, GOLD_MEDIUM_VALUE, 2.0),
        'large': (34, GOLD_LARGE_VALUE, 4.0),
    }
    def __init__(self, x, y, size='medium'):
        radius, value, weight = Gold.SIZES[size]
        super().__init__(x, y, value, weight, radius, f'{size} gold')
        self.size = size
        self._make_blob(9, 0.22)
    def draw(self, surface):
        ...