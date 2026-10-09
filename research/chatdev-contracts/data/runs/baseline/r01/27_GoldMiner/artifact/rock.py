class Rock(GameObject):
    """Worthless-ish stone; heavy, slows the claw down for its small value."""
    SIZES = {'small': dict(radius=16, value=20, weight=3.0),
             'large': dict(radius=24, value=30, weight=5.0)}
    def __init__(self, x, y, size='small'):
        s = self.SIZES[size]
        super().__init__(x, y, s['radius'], s['value'], s['weight'], 'rock')
    def draw(self, surface):
        r = int(self.radius)
        rect = pygame.Rect(int(self.x) - r, int(self.y) - r, 2 * r, 2 * r)
        pygame.draw.circle(surface, ROCK_COLOR, rect.center, r)
        pygame.draw.circle(surface, ROCK_DARK, rect.center, r, 2)
        pygame.draw.circle(surface, (170, 170, 170),
                           (rect.centerx - r // 3, rect.centery - r // 3), max(2, r // 4))