class Bullet:
    """A projectile fired either by the player (upwards) or an alien (downwards)."""
    def __init__(self, x, y, speed, color):
        self.width = settings.BULLET_WIDTH
        self.height = settings.BULLET_HEIGHT
        self.x = x
        self.y = y
        self.speed = speed
        self.color = color
    @property
    def rect(self):
        return pygame.Rect(int(self.x), int(self.y), self.width, self.height)
    def update(self, dt_ms):
        # Speeds are defined per 60fps frame; scale by dt for smoothness.
        self.y += self.speed * (dt_ms / (1000 / settings.FPS))
    def is_offscreen(self):
        return self.y + self.height < 0 or self.y > settings.SCREEN_HEIGHT
    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.rect)