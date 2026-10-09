class Diamond(GameObject):
    """A rare, lightweight gem worth a huge amount of gold."""
    def __init__(self, x, y):
        super().__init__(x, y, 'diamond', S.DIAMOND_VALUE, S.DIAMOND_WEIGHT, S.DIAMOND_RADIUS)
        self.spin = random.uniform(0, math.pi)
    def draw(self, surface):
        r = self.radius
        cx, cy = self.x, self.y
        # classic gem: table on top, point at bottom
        pts = [
            (cx - r, cy - r * 0.35),
            (cx - r * 0.5, cy - r),
            (cx + r * 0.5, cy - r),
            (cx + r, cy - r * 0.35),
            (cx, cy + r),
        ]
        pygame.draw.polygon(surface, S.DIAMOND_DARK, pts)
        pygame.draw.polygon(surface, S.DIAMOND_COLOR, pts, 3)
        # inner facet lines
        pygame.draw.line(surface, S.DIAMOND_DARK, (cx - r*0.5, cy - r), (cx - r*0.25, cy + r*0.1))
        ...