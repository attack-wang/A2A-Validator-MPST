class Explosion:
    """Expanding blast ring shown when TNT detonates."""
    def __init__(self, x, y):
        self.x, self.y = x, y
        self.radius = 10
        self.max_radius = settings.TNT_BLAST_RADIUS
        self.done = False
    def update(self, dt):
        self.radius += 250 * dt
        if self.radius >= self.max_radius:
            self.done = True
    def draw(self, surface):
        r = int(self.radius)
        if r > 0:
            pygame.draw.circle(surface, settings.COLOR_ORANGE, (int(self.x), int(self.y)), r, 4)
            pygame.draw.circle(surface, settings.COLOR_YELLOW, (int(self.x), int(self.y)), max(1, r - 8), 2)