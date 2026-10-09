class Mole(GameObject):
    """Burrowing critter that drifts sideways; medium value, light."""
    def __init__(self, x, y, level=1):
        value = MOLE_VALUE + (level - 1) * 25
        super().__init__(x, y, value, 1.4, 18, 'mole')
        self.speed = random.choice([-1, 1]) * (40 + level * 8)
        self.min_x = OBJECT_MARGIN_X + self.radius
        self.max_x = SCREEN_WIDTH - OBJECT_MARGIN_X - self.radius
    def update(self, dt):
        self.x += self.speed * dt
        self.wobble += dt * 6
        if self.x <= self.min_x:
            self.x = self.min_x
            self.speed = abs(self.speed)
        elif self.x >= self.max_x:
            self.x = self.max_x
            self.speed = -abs(self.speed)
    def draw(self, surface):
        r = self.radius
        pygame.draw.circle(surface, COLOR_MOLE, (int(self.x), int(self.y)), r)
        pygame.draw.circle(surface, COLOR_MOLE_DARK, (int(self.x), int(self.y)), r, 2)
        # eyes and nose
        pygame.draw.circle(surface, COLOR_TEXT, (int(self.x - r*0.3), int(self.y - r*0.2)), 3)
        pygame.draw.circle(surface, COLOR_TEXT, (int(self.x + r*0.3), int(self.y - r*0.2)), 3)
        pygame.draw.circle(surface, (230, 120, 130), (int(self.x), int(self.y + r*0.2)), int(r*0.25))