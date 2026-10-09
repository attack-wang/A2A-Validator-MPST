class Diamond(GameObject):
    """Small, light, extremely valuable."""
    def __init__(self, x, y):
        super().__init__(x, y, 14, 600, 1.0, 'diamond')
    def draw(self, surface):
        cx, cy = self.x, self.y
        r = self.radius
        pts = [(cx, cy - r), (cx + r, cy), (cx, cy + r), (cx - r, cy)]
        pygame.draw.polygon(surface, DIAMOND_COLOR, pts)
        pygame.draw.polygon(surface, DIAMOND_DARK, pts, 2)
        pygame.draw.line(surface, WHITE, (cx, cy - r), (cx, cy + r), 1)