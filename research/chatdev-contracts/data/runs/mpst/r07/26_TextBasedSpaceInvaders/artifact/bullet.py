class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((settings.BULLET_WIDTH, settings.BULLET_HEIGHT), pygame.SRCALPHA)
        self.image.fill(settings.BULLET_COLOR)
        self.rect = self.image.get_rect(center=(x, y))
    def update(self, dt=1):
        self.rect.y += settings.BULLET_SPEED
        if self.rect.bottom < 0:
            self.kill()