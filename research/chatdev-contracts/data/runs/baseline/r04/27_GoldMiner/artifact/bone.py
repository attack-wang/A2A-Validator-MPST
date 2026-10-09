class Bone(GameObject):
    def __init__(self, x, y):
        spec = OBJECT_TYPES['bone']
        super().__init__('bone', x, y, spec['radius'], spec['value'], spec['reel_time'])
    def draw(self, surface):
        cx, cy = int(self.x), int(self.y)
        r = self.radius
        # shaft
        pygame.draw.line(surface, COLOR_BONE, (cx - r, cy), (cx + r, cy), max(3, r // 2))
        # knobs at ends
        for sx in (-1, 1):
            pygame.draw.circle(surface, COLOR_BONE, (cx + sx * r, cy - r // 3), max(3, r // 3))
            pygame.draw.circle(surface, COLOR_BONE, (cx + sx * r, cy + r // 3), max(3, r // 3))