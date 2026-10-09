class Diamond(GameObject):
    def __init__(self, x, y):
        spec = OBJECT_TYPES['diamond']
        super().__init__('diamond', x, y, spec['radius'], spec['value'], spec['reel_time'])
    def draw(self, surface):
        r = self.radius
        cx, cy = int(self.x), int(self.y)
        pts = [(cx, cy - r), (cx + r, cy), (cx, cy + r), (cx - r, cy)]
        pygame.draw.polygon(surface, COLOR_DIAMOND, pts)
        pygame.draw.polygon(surface, (200, 245, 255), [(cx, cy - r), (cx + r, cy), (cx, cy)], 0)  # lighter facet
        pygame.draw.polygon(surface, (40, 120, 160), pts, 2)
        # sparkle
        pygame.draw.line(surface, COLOR_WHITE, (cx - 2, cy - r//2), (cx - 2, cy - r//2 - 4), 1)