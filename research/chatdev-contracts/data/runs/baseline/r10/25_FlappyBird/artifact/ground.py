'''
ground.py
Scrolling ground strip with a repeating diagonal pattern.
'''
import pygame
from settings import (
    SCREEN_HEIGHT, GROUND_HEIGHT, GROUND_STRIPE_WIDTH,
    GROUND_GRASS, GROUND_GRASS_DARK, GROUND_DIRT, GROUND_DIRT_DARK, OUTLINE,
)
class Ground:
    """Scrolling ground: grass edge on top, dirt with diagonal stripes below."""
    def __init__(self):
        self.y = SCREEN_HEIGHT - GROUND_HEIGHT
        self.offset = 0.0
    def update(self, speed):
        self.offset = (self.offset + speed) % GROUND_STRIPE_WIDTH
    def draw(self, surface):
        # dirt base
        dirt_rect = pygame.Rect(0, self.y, SCREEN_WIDTH, GROUND_HEIGHT)
        pygame.draw.rect(surface, GROUND_DIRT, dirt_rect)
        # diagonal pattern on the dirt
        stripe_h = GROUND_HEIGHT - 14
        for x in range(-GROUND_STRIPE_WIDTH, SCREEN_WIDTH + GROUND_STRIPE_WIDTH, GROUND_STRIPE_WIDTH):
            start_x = x - int(self.offset)
            pygame.draw.line(
                surface, GROUND_DIRT_DARK,
                (start_x, self.y + 14),
                (start_x + stripe_h // 2, self.y + GROUND_HEIGHT),
                4,
            )
        # grass strip on top
        grass_rect = pygame.Rect(0, self.y, SCREEN_WIDTH, 14)
        pygame.draw.rect(surface, GROUND_GRASS, grass_rect)
        pygame.draw.rect(surface, OUTLINE, grass_rect, 2)
        # grass notches moving with the scroll
        for x in range(-GROUND_STRIPE_WIDTH * 2, SCREEN_WIDTH + GROUND_STRIPE_WIDTH * 2, GROUND_STRIPE_WIDTH * 2):
            start_x = x - int(self.offset)
            pygame.draw.polygon(
                surface, GROUND_GRASS_DARK,
                [(start_x, self.y + 14), (start_x + 10, self.y), (start_x + 20, self.y + 14)],
            )