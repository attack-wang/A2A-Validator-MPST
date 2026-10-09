'''
objects.py
Collectible items that appear in the mining field.
Defines the GameObject base class plus Gold, Rock, Diamond and Skull
subclasses, each with a concrete draw() implementation (no placeholders).
'''
import math
import random
import pygame
import settings
class GameObject:
    """Base class for every collectible item in the mine."""
    def __init__(self, kind, x, y):
        stats = settings.OBJECT_STATS[kind]
        self.kind = kind
        self.x = x
        self.y = y
        self.radius = stats["radius"]
        self.value = stats["value"]
        self.weight = stats["weight"]
        self.name = kind.replace("_", " ").title()
    def contains_point(self, px, py, extra=0.0):
        """True if (px, py) lies within radius+extra of this object's centre."""
        dx = px - self.x
        dy = py - self.y
        return dx * dx + dy * dy <= (self.radius + extra) ** 2
    def draw(self, surface):
        """Default rendering: a plain circle coloured by value sign.
        Subclasses override this with richer artwork."""
        color = settings.GOLD_YELLOW if self.value >= 0 else settings.RED
        pygame.draw.circle(surface, color,
                           (int(self.x), int(self.y)), self.radius)
        pygame.draw.circle(surface, settings.BLACK,
                           (int(self.x), int(self.y)), self.radius, 2)
class Gold(GameObject):
    """Gold nugget. Polygon shape stored as RELATIVE offsets so the nugget
    follows the claw correctly while being reeled in."""
    def __init__(self, kind, x, y):
        super().__init__(kind, x, y)
        rng = random.Random(int(x * 31 + y * 17))
        n = 9
        self.shape = []
        for i in range(n):
            ang = 2 * math.pi * i / n
            r = self.radius * rng.uniform(0.75, 1.1)
            self.shape.append((math.cos(ang) * r, math.sin(ang) * r))
    def draw(self, surface):
        pts = [(int(self.x + dx), int(self.y + dy)) for dx, dy in self.shape]
        pygame.draw.polygon(surface, settings.GOLD_YELLOW, pts)
        pygame.draw.polygon(surface, settings.GOLD_DARK, pts, 2)
        # small sparkle
        pygame.draw.circle(surface, settings.WHITE,
                           (int(self.x - self.radius * 0.3),
                            int(self.y - self.radius * 0.3)), 2)
class Rock(GameObject):
    """Heavy, low-value rock: mostly a time-wasting obstacle."""
    def draw(self, surface):
        cx, cy = int(self.x), int(self.y)
        pygame.draw.circle(surface, settings.GRAY, (cx, cy), self.radius)
        pygame.draw.circle(surface, settings.GRAY_DARK, (cx, cy), self.radius, 2)
        pygame.draw.circle(surface, settings.GRAY_DARK,
                           (cx - self.radius // 3, cy - self.radius // 4),
                           max(2, self.radius // 5))
class Diamond(GameObject):
    """Rare, lightweight, very valuable diamond."""
    def draw(self, surface):
        r = self.radius
        cx, cy = int(self.x), int(self.y)
        pts = [(cx, cy - r), (cx + r, cy), (cx, cy + r), (cx - r, cy)]
        pygame.draw.polygon(surface, settings.CYAN, pts)
        pygame.draw.polygon(surface, settings.BLACK, pts, 2)
        pygame.draw.line(surface, settings.WHITE,
                         (cx - r // 2, cy - r // 2), (cx + r // 2, cy - r // 2), 1)
class Skull(GameObject):
    """Dangerous skull: negative value, penalises the player when collected."""
    def draw(self, surface):
        cx, cy = int(self.x), int(self.y)
        r = self.radius
        pygame.draw.circle(surface, settings.WHITE, (cx, cy), r)
        pygame.draw.circle(surface, settings.BLACK, (cx, cy), r, 2)
        eye = max(2, r // 4)
        pygame.draw.circle(surface, settings.BLACK, (cx - r // 3, cy - r // 5), eye)
        pygame.draw.circle(surface, settings.BLACK, (cx + r // 3, cy - r // 5), eye)
        # jaw / teeth
        pygame.draw.line(surface, settings.BLACK,
                         (cx - r // 3, cy + r // 2), (cx + r // 3, cy + r // 2), 2)
        for i in range(-1, 2):
            pygame.draw.line(surface, settings.BLACK,
                             (cx + i * r // 4, cy + r // 2),
                             (cx + i * r // 4, cy + r // 2 + 4), 1)