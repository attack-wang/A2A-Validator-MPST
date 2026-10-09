"""GameObject classes: gold nuggets, rocks, diamonds, TNT, bones, mystery bags."""
import math
import random
import pygame
from settings import *
class GameObject:
    """Base class for every grabbable item buried in the mine."""
    def __init__(self, x, y, radius, value, weight, kind):
        self.x = x
        self.y = y
        self.radius = radius
        self.value = value
        self.weight = weight
        self.kind = kind
        self.alive = True
        self.grabbed = False
    @property
    def pos(self):
        return (self.x, self.y)
    def distance_to(self, px, py):
        return math.hypot(px - self.x, py - self.y)
    def draw(self, surface):
        raise NotImplementedError
class Gold(GameObject):
    """Irregular gold nugget; value scales with size, weight slows reel-in."""
    SIZES = {
        'small':  dict(radius=12, value=50,  weight=1.5),
        'medium': dict(radius=18, value=100, weight=2.5),
        'large':  dict(radius=26, value=250, weight=4.0),
    }
    def __init__(self, x, y, size='medium'):
        s = self.SIZES[size]
        super().__init__(x, y, s['radius'], s['value'], s['weight'], 'gold')
        self.points = self._make_points()
    def _make_points(self):
        pts = []
        n = 9
        for i in range(n):
            ang = i * 2 * math.pi / n
            r = self.radius * random.uniform(0.8, 1.05)
            pts.append((math.cos(ang) * r, math.sin(ang) * r))
        return pts
    def draw(self, surface):
        cx, cy = self.x, self.y
        pts = [(cx + px, cy + py) for (px, py) in self.points]
        pygame.draw.polygon(surface, GOLD_COLOR, pts)
        pygame.draw.polygon(surface, GOLD_DARK, pts, 2)
        pygame.draw.circle(surface, (255, 240, 160),
                           (int(cx - self.radius * 0.3), int(cy - self.radius * 0.3)),
                           max(2, int(self.radius * 0.2)))