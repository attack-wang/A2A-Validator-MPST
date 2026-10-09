class Gold(GameObject):
    NAME = "gold"
    SIZES = {
        'small': {'radius': 12, 'value': 50, 'weight': 0.6},
        'medium': {'radius': 18, 'value': 150, 'weight': 1.0},
        'large': {'radius': 26, 'value': 350, 'weight': 1.8},
    }
    def __init__(self, x, y, size='medium'):
        spec = self.SIZES[size]
        self.size = size
        self.radius = spec['radius']
        self.value = spec['value']
        self.weight = spec['weight']
        super().__init__(x, y)  # careful: super sets defaults then we override