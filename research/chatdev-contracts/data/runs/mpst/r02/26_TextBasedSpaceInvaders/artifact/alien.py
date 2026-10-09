'''A single alien in the invading fleet.'''
import pygame
from settings import ALIEN_WIDTH, ALIEN_HEIGHT, ALIEN_POINTS, WHITE
class Alien(pygame.sprite.Sprite):
    '''One alien invader drawn as a simple pixel-style creature.'''
    def __init__(self, x, y, row):
        super().__init__()
        self.row = row
        self.points = ALIEN_POINTS[row] if row < len(ALIEN_POINTS) else ALIEN_POINTS[-1]
        self.image = pygame.Surface((ALIEN_WIDTH, ALIEN_HEIGHT), pygame.SRCALPHA)
        self._draw_alien(row)
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
    def _draw_alien(self, row):
        '''Draw a blocky alien whose color depends on its row.'''
        colors = [(255, 80, 80), (255, 200, 60), (120, 220, 120), (120, 160, 255)]
        color = colors[row % len(colors)]
        w, h = ALIEN_WIDTH, ALIEN_HEIGHT
        # body
        pygame.draw.rect(self.image, color, (4, 6, w - 8, h - 12))
        # eyes
        pygame.draw.rect(self.image, (10, 10, 30), (10, 10, 6, 6))
        pygame.draw.rect(self.image, (10, 10, 30), (w - 16, 10, 6, 6))
        # legs / antennae
        pygame.draw.rect(self.image, color, (8, h - 6, 6, 6))
        pygame.draw.rect(self.image, color, (w - 14, h - 6, 6, 6))
        pygame.draw.rect(self.image, color, (w // 2 - 3, 0, 6, 6))