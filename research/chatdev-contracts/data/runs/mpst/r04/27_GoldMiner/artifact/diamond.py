class Diamond(GameObject):
    """Light, extremely valuable gem."""
    def __init__(self, x, y):
        radius, value, weight = settings.GOLD_SPECS["diamond"]
        super().__init__(x, y, "diamond", radius, value, weight,
                         settings.COLOR_DIAMOND, settings.COLOR_DIAMOND_DARK)
    def draw(self, surface):
        pos = self.pos
        r = self.radius
        pts = [(pos[0], pos[1] - r), (pos[0] + r, pos[1]), (pos[0], pos[1] + r), (pos[0] - r, pos[1])]
        pygame.draw.polygon(surface, self.color, pts)
        pygame.draw.polygon(surface, self.dark_color, pts, 2)
        pygame.draw.line(surface, settings.COLOR_WHITE, (pos[0] - r // 2, pos[1] - r // 2), (pos[0], pos[1] - r), 1)