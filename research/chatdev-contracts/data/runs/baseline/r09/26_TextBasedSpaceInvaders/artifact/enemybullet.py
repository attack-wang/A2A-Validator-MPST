class Bullet:
    """Base projectile moving vertically; subclasses set direction."""
    def __init__(self, settings, screen, x, y):
        self.settings = settings
        self.screen = screen
        self.image = pygame.Surface((settings.BULLET_WIDTH, settings.BULLET_HEIGHT))
        self.rect = self.image.get_rect(centerx=x, centery=y)
        self.y = float(self.rect.y)
        self.speed = 0.0
    def update(self, dt):
        self.y += self.speed * dt
        self.rect.y = round(self.y)
    def off_screen(self):
        return self.rect.bottom < 0 or self.rect.top > self.settings.SCREEN_HEIGHT
    def draw(self):
        self.screen.blit(self.image, self.rect)
class PlayerBullet(Bullet):
    def __init__(...):
        super().__init__(...)
        self.speed = -settings.BULLET_SPEED
        self.image.fill(settings.COLOR_BULLET)
class EnemyBullet(Bullet):
    def __init__(...):
        super().__init__(...)
        self.speed = settings.ENEMY_BULLET_SPEED
        self.image.fill(settings.COLOR_ENEMY_BULLET)