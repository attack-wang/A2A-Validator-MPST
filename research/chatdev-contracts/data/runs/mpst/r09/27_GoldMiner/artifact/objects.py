'''
objects.py
Definition of the collectible items that appear in the mine.
'''
import math
import random
import pygame
import config
class GameObject:
    """An item lying in the mine that the claw can grab."""
    def __init__(self, x, y, name, value, weight, radius, color, kind):
        self.x = x
        self.y = y
        self.name = name
        self.value = value
        self.weight = weight      # determines reel-in time
        self.radius = radius
        self.color = color
        self.kind = kind          # 'gold', 'rock', 'tnt', ...
        self.grabbed = False      # currently attached to the claw
        self.collected = False    # removed from the field
    @property
    def reel_time(self):
        """Relative time it takes to reel this object in (seconds-ish)."""
        return self.weight
    def collides_with(self, px, py, claw_radius):
        return math.hypot(px - self.x, py - self.y) <= self.radius + claw_radius
    def draw(self, surface):
        raise NotImplementedError
    # helpers ---------------------------------------------------------------
    def _draw_circle(self, surface, color, radius=None):
        r = radius or self.radius
        pygame.draw.circle(surface, color, (int(self.x), int(self.y)), int(r))
class Gold(GameObject):
    """A gold nugget. Bigger nuggets are worth more but reel in slowly."""
    def __init__(self, x, y, size="small"):
        spec = {"small": config.GOLD_SMALL,
                "medium": config.GOLD_MEDIUM,
                "large": config.GOLD_LARGE}[size]
        super().__init__(x, y, spec["name"], spec["value"], spec["weight"], spec["radius"], config.COLOR_GOLD, "gold")
        self.size = size
    def draw(self, surface):
        # nugget: irregular polygon-ish circle with shine
        ...