class Rock(GameObject):
    def __init__(self, kind, x, y):
        super().__init__(kind, x, y)
        points = []
        n = 8
        for i in range(n):
            ang = math.tau * i / n
            r = self.radius * random.uniform(0.85, 1.1)
            points.append((math.cos(ang) * r, math.sin(ang) * r))
        self.outline = points
    def draw(self, surface):
        pts = [(self.x + px, self.y + py) for px, py in self.outline]
        pygame.draw.polygon(surface, config.COLOR_ROCK, pts)
        pygame.draw.polygon(surface, config.COLOR_ROCK_DARK, pts, 2)
        # crack
        pygame.draw.line(surface, config.COLOR_ROCK_DARK, (self.x - self.radius*0.4, self.y - self.radius*0.2), (self.x + self.radius*0.1, self.y + self.radius*0.3), 2)
class RockSmall(Rock):
    def __init__(self, x, y):
        super().__init__("rock_small", x, y)
class RockLarge(Rock):
    def __init__(self, x, y):
        super().__init__("rock_large", x, y)