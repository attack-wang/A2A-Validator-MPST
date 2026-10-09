class GoldNugget(GameObject):
    def __init__(self, kind, x, y):
        super().__init__(kind, x, y)
        points = []
        n = 9
        for i in range(n):
            ang = math.tau * i / n
            r = self.radius * random.uniform(0.82, 1.12)
            points.append((math.cos(ang) * r, math.sin(ang) * r))
        self.outline = points
    def draw(self, surface):
        pts = [(self.x + px, self.y + py) for px, py in self.outline]
        pygame.draw.polygon(surface, config.COLOR_GOLD_DARK, pts)
        inner = [(self.x + px * 0.7, self.y + py * 0.7 - self.radius * 0.15) for px, py in self.outline]
        pygame.draw.polygon(surface, config.COLOR_GOLD, inner)
        # sparkle
        pygame.draw.circle(surface, (255, 255, 220), (int(self.x - self.radius*0.3), int(self.y - self.radius*0.3)), max(2, self.radius // 5))
class GoldSmall(GoldNugget):
    def __init__(self, x, y):
        super().__init__("gold_small", x, y)
class GoldMedium(GoldNugget):
    def __init__(self, x, y):
        super().__init__("gold_medium", x, y)
class GoldLarge(GoldNugget):
    def __init__(self, x, y):
        super().__init__("gold_large", x, y)