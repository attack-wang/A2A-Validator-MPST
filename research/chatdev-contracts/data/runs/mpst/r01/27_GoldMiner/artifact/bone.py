class Bone(GameObject):
    def __init__(self, x, y):
        super().__init__("bone", x, y)
        self.angle = random.uniform(0, math.pi)
    def draw(self, surface):
        # draw a bone: shaft with two knobs at each end
        length = self.radius * 2.4
        dx = math.cos(self.angle) * length / 2
        dy = math.sin(self.angle) * length / 2
        x1, y1 = self.x - dx, self.y - dy
        x2, y2 = self.x + dx, self.y + dy
        pygame.draw.line(surface, config.COLOR_BONE, (x1, y1), (x2, y2), 5)
        knob = max(3, self.radius // 3)
        for (kx, ky) in ((x1, y1), (x2, y2)):
            for off in (-1, 1):
                px = kx + math.cos(self.angle + math.pi/2) * off * knob * 0.8
                py = ky + math.sin(self.angle + math.pi/2) * off * knob * 0.8
                pygame.draw.circle(surface, config.COLOR_BONE, (int(px), int(py)), knob)