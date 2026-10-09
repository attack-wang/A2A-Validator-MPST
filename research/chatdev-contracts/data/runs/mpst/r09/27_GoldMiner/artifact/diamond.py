class Diamond(GameObject):
    """A rare, high-value gem: light to reel in but hard to aim at."""
    def __init__(self, x, y):
        spec = config.DIAMOND
        super().__init__(x, y, spec["name"], spec["value"], spec["weight"],
                         spec["radius"], config.COLOR_DIAMOND, "diamond")
    def draw(self, surface):
        cx, cy = int(self.x), int(self.y)
        r = self.radius
        pts = [(cx, cy - r * 1.4), (cx + r, cy - r * 0.2),
               (cx, cy + r * 1.4), (cx - r, cy - r * 0.2)]
        pygame.draw.polygon(surface, self.color, pts)
        pygame.draw.polygon(surface, (60, 150, 200), pts, 2)
        pygame.draw.line(surface, (230, 250, 255), (cx, cy - r), (cx, cy + r), 1)
        pygame.draw.line(surface, (230, 250, 255), (cx - r, cy - r // 5), (cx + r, cy - r // 5), 1)