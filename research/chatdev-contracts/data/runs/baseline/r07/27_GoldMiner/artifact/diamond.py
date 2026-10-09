class Diamond(GameObject):
    """Rare, light and very valuable gem."""
    def __init__(self, x, y):
        super().__init__(x, y, 600, 1.0, 14, 'diamond')
        self.points = [(-14, 0), (0, -16), (14, 0), (0, 16)]
    def draw(self, surface):
        cx, cy = int(self.x), int(self.y)
        pts = [(cx + px, cy + py) for px, py in self.points]
        pygame.draw.polygon(surface, DIAMOND_COLOR, pts)
        pygame.draw.polygon(surface, DIAMOND_DARK, pts, 2)
        pygame.draw.line(surface, WHITE, (cx - 6, cy - 7), (cx + 2, cy + 3), 2)