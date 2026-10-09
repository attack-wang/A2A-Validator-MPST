'''
ground.py
Scrolling ground strip at the bottom of the screen. Provides collision
with the bird and scrolls at the current pipe speed.
'''
import pygame
import settings
class Ground:
    def __init__(self):
        self.y = settings.SKY_HEIGHT
        self.offset = 0.0
        self.image = self._build_image()
    @staticmethod
    def _build_image():
        img = pygame.Surface((settings.SCREEN_WIDTH + 48, settings.GROUND_HEIGHT))
        img.fill(settings.GROUND_DIRT)
        # grass strip
        pygame.draw.rect(img, settings.GROUND_GRASS, (0, 0, img.get_width(), 12))
        # diagonal pattern on dirt
        for i in range(-settings.GROUND_HEIGHT, img.get_width() + settings.GROUND_HEIGHT, 24):
            pygame.draw.line(img, settings.GROUND_DIRT_DARK, (i, 14), (i + 20, settings.GROUND_HEIGHT), 6)
        # top edge line
        pygame.draw.rect(img, settings.GROUND_EDGE, (0, 0, img.get_width(), 3))
        return img
    def update(self, dt, speed):
        self.offset = (self.offset + speed * dt) % 24
    def collides(self, bird_rect):
        return bird_rect.bottom >= self.y
    def draw(self, surface):
        surface.blit(self.image, (-self.offset, self.y))