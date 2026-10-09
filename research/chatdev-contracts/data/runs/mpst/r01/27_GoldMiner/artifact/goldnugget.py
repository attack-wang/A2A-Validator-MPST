class GoldNugget(GameObject):
    def __init__(self, kind, x, y):
        super().__init__(kind, x, y)
        # Pre-generate an irregular nugget outline so it looks hand-drawn.
        points = []
        n = 9
        for i in range(n):
            ang = math.tau * i / n
            r = self.radius * random.uniform(0.82, 1.12)
            points.append((math.cos(ang) * r, math.sin(ang) * r))
        self.outline = points
    def draw(self, surface):
        pts = [(self.x + px, self.y + py) for px, py in self.outline]
        pygame.draw.polygon(surface, config.COLOR_GOLD_DARK, pts, 0)  # shadow? 
        ...