class Diamond(GameObject):
    """Rare gem: small, light and extremely valuable."""
    def __init__(self, x, y, level=1):
        value = DIAMOND_VALUE + (level - 1) * 50
        super().__init__(x, y, value, 1.2, 20, 'diamond')
    def draw(self, surface):
        r = self.radius
        pts = [(self.x, self.y - r), (self.x + r * 0.8, self.y),
               (self.x, self.y + r), (self.x - r * 0.8, self.y)]
        pygame.draw.polygon(surface, COLOR_DIAMOND, pts)
        pygame.draw.polygon(surface, COLOR_DIAMOND_DARK, pts, 3)
        # facet lines
        pygame.draw.line(surface, COLOR_WHITE, (self.x, self.y - r), (self.x, self.y + r), 1)
        pygame.draw.line(surface, COLOR_WHITE, (self.x - r * 0.8, self.y), (self.x + r * 0.8, self.y), 1)