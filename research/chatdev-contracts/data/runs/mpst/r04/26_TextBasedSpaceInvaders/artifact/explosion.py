'''Explosion effect sprite for the Space Invaders game.'''
import pygame
class Explosion(pygame.sprite.Sprite):
    '''A short-lived expanding ring shown when something is destroyed.'''
    def __init__(self, center, color):
        super().__init__()
        self.center = center
        self.radius = 2
        self.max_radius = 18
        self.color = color
        self.image = self._make_image()
        self.rect = self.image.get_rect(center=self.center)
    def _make_image(self):
        size = self.max_radius * 2
        surf = pygame.Surface((size, size), pygame.SRCALPHA)
        pygame.draw.circle(surf, self.color,
                           (self.max_radius, self.max_radius), self.radius, 2)
        return surf
    def update(self):
        self.radius += 2
        if self.radius > self.max_radius:
            self.kill()
            return
        self.image = self._make_image()
        self.rect = self.image.get_rect(center=self.center)