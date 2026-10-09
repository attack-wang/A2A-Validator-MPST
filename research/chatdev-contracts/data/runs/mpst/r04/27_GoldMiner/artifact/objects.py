class Gold(GameObject):
    """Lumpy gold nugget; value and weight scale with size."""
    def __init__(self, x, y, size):
        radius, value, weight = settings.GOLD_SPECS[size]
        super().__init__(x, y, size, radius, value, weight,
                         settings.COLOR_GOLD, settings.COLOR_GOLD_DARK)
    def draw(self, surface):
        pos = self.pos
        r = self.radius
        pygame.draw.circle(surface, self.color, pos, r)
        pygame.draw.circle(surface, self.color,
                           (pos[0] - r // 2, pos[1] - r // 3), max(3, int(r * 0.55)))
        pygame.draw.circle(surface, self.color,
                           (pos[0] + r // 2, pos[1] - r // 4), max(2, int(r * 0.4)))
        pygame.draw.circle(surface, self.dark_color, pos, r, 2)
        # shine
        pygame.draw.circle(surface, settings.COLOR_WHITE,
                           (pos[0] - r // 3, pos[1] - r // 2), max(1, r // 6))