class Bomb(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((settings.BOMB_WIDTH, settings.BOMB_HEIGHT), pygame.SRCALPHA)
        self.image.fill(settings.BOMB_COLOR)
        self.rect = self.image.get_rect(center=(x, y))
    def update(self, dt=1):
        self.rect.y += settings.BOMB_SPEED
        if self.rect.top > settings.HEIGHT:
            self.kill()