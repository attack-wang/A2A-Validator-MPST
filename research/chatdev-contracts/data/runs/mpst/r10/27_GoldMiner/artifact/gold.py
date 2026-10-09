class Gold(GameObject):
    def __init__(self, kind, x, y):
        super().__init__(kind, x, y)
    def _draw(self, surface, x, y):
        r = self.radius
        # body
        pygame.draw.circle(surface, GOLD_COLOR, (x, y), r)
        pygame.draw.circle(surface, GOLD_DARK, (x, y), r, 2)
        # shine
        pygame.draw.circle(surface, GOLD_SHINE, (x - r//3, y - r//3), max(2, r//4))