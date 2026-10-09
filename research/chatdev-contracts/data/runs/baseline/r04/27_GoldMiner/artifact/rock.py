class Rock(GameObject):
    def __init__(self, size, x, y):
        kind = f'rock_{size}'
        spec = OBJECT_TYPES[kind]
        super().__init__(kind, x, y, spec['radius'], spec['value'], spec['reel_time'])
        self.size = size
        self.points = self._make_blob()
    def _make_blob(self):
        rnd = random.Random(int(self.x * 733 + self.y * 977))
        n = 9
        pts = []
        for i in range(n):
            ang = (i / n) * math.tau
            rad = self.radius * rnd.uniform(0.75, 1.05)
            pts.append((math.cos(ang) * rad, math.sin(ang) * rad))
        return pts
    def draw(self, surface):
        cx, cy = int(self.x), int(self.y)
        pts = [(cx + px, cy + py) for px, py in self.points]
        pygame.draw.polygon(surface, COLOR_ROCK_DARK, pts)
        inner = [(cx + px * 0.7, cy + py * 0.7 - 2) for px, py in self.points]
        pygame.draw.polygon(surface, COLOR_ROCK, inner)