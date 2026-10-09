class Rock(GameObject):
    """Heavy, low-value rock that slows the reel-in."""
    def __init__(self, x, y, large):
        kind = "rock_large" if large else "rock_small"
        radius, value, weight = settings.GOLD_SPECS[kind]
        super().__init__(x, y, kind, radius, value, weight,
                         settings.COLOR_ROCK, settings.COLOR_ROCK_DARK)
    def draw(self, surface):
        pos = self.pos
        r = self.radius
        pygame.draw.circle(surface, self.color, pos, r)
        # facets
        pygame.draw.polygon(surface, self.dark_color, [
            (pos[0] - r // 2, pos[1] + r // 3),
            (pos[0] + r // 3, pos[1] + r // 2),
            (pos[0] + r // 2, pos[1]),
        ])
        pygame.draw.circle(surface, self.dark_color, pos, r, 2)