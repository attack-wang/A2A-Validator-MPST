class Candy:
    SHAPES = ['circle', 'square', 'diamond', 'triangle', 'hexagon', 'oval']
    COLORS = [...]  # 6 colors
    TYPES = list of (color, shape) tuples
    def __init__(self, type_idx, special=None):
        self.type_idx = type_idx
        self.special = special
        self.offset_x = 0.0
        self.offset_y = 0.0
        self.clearing = False
        self.clear_progress = 0.0
        self.spawn_scale = 1.0