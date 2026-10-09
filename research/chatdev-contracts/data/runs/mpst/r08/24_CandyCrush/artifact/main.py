class Candy:
    TYPES = ...  # list of (color, shape)
    def __init__(self, type_idx):
        self.type_idx = type_idx
        self.special = None  # None, 'striped_h', 'striped_v', 'wrapped', 'bomb'
        self.offset_x = 0.0  # pixel offset for animation
        self.offset_y = 0.0
        self.clearing = False
        self.clear_timer = 0.0
        self.scale = 1.0