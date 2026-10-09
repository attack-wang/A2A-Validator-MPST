'''Parallax scrolling background: sky gradient, clouds, hills, and ground.'''
import random
import pygame
from settings import (SCREEN_WIDTH, SCREEN_HEIGHT, GROUND_HEIGHT,
                      SKY_TOP, SKY_BOTTOM)
class Cloud:
    """A simple drifting cloud sprite."""
    def __init__(self, x, y, speed_scale):
        """Build a cloud surface and set its drift parameters."""
        self.x = x
        self.y = y
        self.speed_scale = speed_scale
        self.surface = self._make_surface()
    @staticmethod
    def _make_surface():
        """Draw a puffy cloud from overlapping ellipses."""
        w, h = 90, 36
        surf = pygame.Surface((w, h), pygame.SRCALPHA)
        pygame.draw.ellipse(surf, (255, 255, 255), (0, 12, 40, 22))
        pygame.draw.ellipse(surf, (255, 255, 255), (18, 4, 44, 28))
        pygame.draw.ellipse(surf, (255, 255, 255), (46, 12, 42, 22))
        return surf
    def update(self, speed):
        """Drift left at a fraction of the world speed; wrap to the right edge."""
        self.x -= speed * self.speed_scale
        if self.x < -self.surface.get_width():
            self.x = SCREEN_WIDTH + random.randint(0, 120)
            self.y = random.randint(30, SCREEN_HEIGHT // 2)
    def draw(self, surface):
        """Blit the cloud at its current position."""
        surface.blit(self.surface, (int(self.x), int(self.y)))
class ScrollingBackground:
    """Sky gradient with parallax clouds, hills, and a scrolling ground."""
    def __init__(self):
        """Pre-render the sky, hills, and ground; scatter initial clouds."""
        self.sky = self._make_sky()
        self.hills = self._make_hills()
        self.ground = self._make_ground()
        self.hills_x = 0
        self.ground_x = 0
        self.clouds = [Cloud(random.uniform(0, SCREEN_WIDTH),
                             random.randint(30, SCREEN_HEIGHT // 2),
                             random.uniform(0.15, 0.35))
                       for _ in range(5)]
    @staticmethod
    def _make_sky():
        """Render the vertical sky gradient once."""
        sky = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        for y in range(SCREEN_HEIGHT):
            t = y / (SCREEN_HEIGHT - 1)
            color = tuple(int(SKY_TOP[i] + (SKY_BOTTOM[i] - SKY_TOP[i]) * t)
                          for i in range(3))
            pygame.draw.line(sky, color, (0, y), (SCREEN_WIDTH, y))
        return sky
    @staticmethod
    def _make_hills():
        """Render a repeating strip of soft green hills."""
        w, h = 240, 60
        strip = pygame.Surface((w, h), pygame.SRCALPHA)
        pygame.draw.ellipse(strip, (126, 200, 116), (-40, 18, 160, 90))
        pygame.draw.ellipse(strip, (110, 185, 105), (80, 26, 200, 80))
        return strip
    @staticmethod
    def _make_ground():
        """Render a repeating grass-and-dirt ground tile."""
        w, h = 48, GROUND_HEIGHT
        tile = pygame.Surface((w, h))
        tile.fill((222, 184, 121))  # dirt
        pygame.draw.rect(tile, (120, 200, 90), (0, 0, w, 22))       # grass
        pygame.draw.rect(tile, (90, 160, 70), (0, 18, w, 4))        # grass edge
        pygame.draw.rect(tile, (200, 160, 100), (0, 30, w, 6))      # dirt band
        pygame.draw.line(tile, (180, 140, 90), (0, 44), (w, 44), 2)
        return tile
    def update(self, speed):
        """Scroll hills and ground; clouds drift with light parallax."""
        for cloud in self.clouds:
            cloud.update(speed)
        self.hills_x = (self.hills_x - speed * 0.3) % self.hills.get_width()
        self.ground_x = (self.ground_x - speed) % self.ground.get_width()
    def draw(self, surface):
        """Draw sky, clouds, hills, and tiled ground in back-to-front order."""
        surface.blit(self.sky, (0, 0))
        for cloud in self.clouds:
            cloud.draw(surface)
        hill_w = self.hills.get_width()
        y = SCREEN_HEIGHT - GROUND_HEIGHT - self.hills.get_height()
        x = -int(self.hills_x)
        while x < SCREEN_WIDTH:
            surface.blit(self.hills, (x, y))
            x += hill_w
        ground_w = self.ground.get_width()
        gy = SCREEN_HEIGHT - GROUND_HEIGHT
        x = -int(self.ground_x)
        while x < SCREEN_WIDTH:
            surface.blit(self.ground, (x, gy))
            x += ground_w