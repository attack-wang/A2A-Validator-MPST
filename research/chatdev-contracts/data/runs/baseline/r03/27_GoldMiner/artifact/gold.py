"""
gold.py
Gold nuggets: the primary target of the game...
"""
import math
import random
import pygame
import settings as S
from objects import GameObject
class Gold(GameObject):
    """A gold nugget. size in {'small', 'medium', 'large'}."""
    def __init__(self, x, y, size):
        cfg = {
            'small': (S.GOLD_SMALL_VALUE, S.GOLD_SMALL_WEIGHT, S.GOLD_SMALL_RADIUS),
            'medium': (S.GOLD_MEDIUM_VALUE, S.GOLD_MEDIUM_WEIGHT, S.GOLD_MEDIUM_RADIUS),
            'large': (S.GOLD_LARGE_VALUE, S.GOLD_LARGE_WEIGHT, S.GOLD_LARGE_RADIUS),
        }[size]
        super().__init__(x, y, 'gold_' + size, *cfg)
        self.size = size
        # random blob shape: radii offsets for a lumpy circle
        self.blob = [random.uniform(0.82, 1.12) for _ in range(10)]
    def draw(self, surface):
        pts = []
        n = len(self.blob)
        for i, k in enumerate(self.blob):
            ang = i / n * 2 * math.pi
            r = self.radius * k
            pts.append((self.x + math.cos(ang) * r, self.y + math.sin(ang) * r))
        pygame.draw.polygon(surface, S.GOLD_DARK, pts)
        pygame.draw.polygon(surface, S.GOLD_COLOR, pts, 3)
        # shine highlight
        shine_r = self.radius * 0.45
        pygame.draw.circle(surface, S.GOLD_SHINE,
                           (int(self.x - self.radius * 0.3), int(self.y - self.radius * 0.3)),
                           max(2, int(shine_r)))