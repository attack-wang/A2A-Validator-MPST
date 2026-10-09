class Rock(GameObject):
    """Heavy, nearly worthless obstacle. Slows the claw down badly."""
    SPECS = {
        'small': {'value': 20, 'weight': 4.0, 'radius': 20},
        'large': {'value': 30, 'weight': 7.0, 'radius': 30},
    }
    def __init__(self, x, y, size):
        spec = self.SPECS[size]
        super().__init__(x, y, spec['value'], spec['weight'], spec['radius'], 'rock')
        self.size = size
        self.points = self._make_rock()
    def _make_rock(self):
        pts = []
        n = 8
        for i in range(n):
            ang = math.tau * i / n
            r = self.radius * random.uniform(0.8, 1.1)
            pts.append((math.cos(ang) * r, math.sin(ang) * r))
        return pts
    def draw(self, surface):
        cx, cy = int(self.x), int(self.y)
        pts = [(cx + px, cy + py) for px, py in self.points]
        pygame.draw.polygon(surface, ROCK_COLOR, pts)
        pygame.draw.polygon(surface, ROCK_DARK, pts, 2)
        pygame.draw.circle(surface, ROCK_DARK, (cx + self.radius // 3, cy - self.radius // 4), max(2, self.radius // 6))