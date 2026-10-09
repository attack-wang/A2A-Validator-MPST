'''
Ground class: the scrolling floor the bird must avoid.
'''
import pygame
import settings
class Ground:
    '''The scrolling floor the bird must avoid.'''
    def __init__(self):
        self.y = settings.WINDOW_HEIGHT - settings.GROUND_HEIGHT
        self.offset = 0.0
    def update(self, speed):
        """Scroll the ground pattern to the left."""
        self.offset = (self.offset + speed) % 24  # pattern width
    def collides(self, bird_rect):
        return bird_rect.bottom >= self.y
    def draw(self, surface):
        pygame.draw.rect(surface, settings.GROUND_BODY,
                         (0, self.y, settings.WINDOW_WIDTH, settings.GROUND_HEIGHT))
        # grass strip
        pygame.draw.rect(surface, settings.GROUND_TOP, (0, self.y, settings.WINDOW_WIDTH, 12))
        # diagonal stripes on grass
        stripe_w = 12
        for i in range(-1, settings.WINDOW_WIDTH // stripe_w + 2):
            x = i * stripe_w - self.offset
            pygame.draw.polygon(surface, settings.GROUND_LINE,
                                [(x, self.y),
                                 (x + stripe_w / 2, self.y),
                                 (x + stripe_w / 2 - 6, self.y + 12),
                                 (x - 6, self.y + 12)])
        # dirt shading
        pygame.draw.rect(surface, settings.GROUND_DARK, (0, self.y + 12, settings.WINDOW_WIDTH, 4))
        pygame.draw.line(surface, settings.GROUND_DARK, (0, self.y + 24),
                         (settings.WINDOW_WIDTH, self.y + 24), 2)