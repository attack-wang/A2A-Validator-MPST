'''
Game objects (gold, rocks, diamonds, TNT, bones) for the Gold Miner game.
'''
import math
import random
import pygame
from config import (OBJECT_TYPES, COLOR_GOLD, COLOR_GOLD_DARK, COLOR_ROCK,
                    COLOR_ROCK_DARK, COLOR_DIAMOND, COLOR_DIAMOND_DARK,
                    COLOR_TNT, COLOR_TNT_DARK, COLOR_BONE, COLOR_LABEL,
                    COLOR_TEXT)
class GameObject:
    """A collectible item in the mine with a value, weight and position."""
    def __init__(self, kind, x, y):
        props = OBJECT_TYPES[kind]
        self.kind = kind
        self.x = x
        self.y = y
        self.radius = props["radius"]
        self.value = props["value"]
        self.weight = props["weight"]
        self.alive = True     # False once delivered, destroyed or removed
        self.grabbed = False  # True while hanging on the claw
        self.wobble = random.uniform(0, math.tau)  # for subtle animation
    @property
    def position(self):
        """Current (x, y) position as a tuple."""
        return (self.x, self.y)
    def draw(self, surface):
        """Dispatch to the per-kind drawing routine."""
        {
            "gold_small": self._draw_gold,
            "gold_medium": self._draw_gold,
            "gold_large": self._draw_gold,
            "diamond": self._draw_diamond,
            "rock_small": self._draw_rock,
            "rock_large": self._draw_rock,
            "bone": self._draw_bone,
            "tnt": self._draw_tnt,
        }[self.kind](surface)
    def _draw_gold(self, surface):
        r = self.radius
        pygame.draw.circle(surface, COLOR_GOLD, (int(self.x), int(self.y)), r)
        pygame.draw.circle(surface, COLOR_GOLD_DARK, (int(self.x), int(self.y)), r, 2)
        # small shine highlight
        pygame.draw.circle(surface, (255, 240, 180),
                           (int(self.x - r * 0.35), int(self.y - r * 0.35)),
                           max(2, int(r * 0.25)))
        # "$" nugget facets
        ...
    def _draw_diamond(self, surface):
        r = self.radius
        cx, cy = self.x, self.y
        points = [(cx, cy - r), (cx + r, cy), (cx, cy + r), (cx - r, cy)]
        pygame.draw.polygon(surface, COLOR_DIAMOND, points)
        pygame.draw.polygon(surface, COLOR_DIAMOND_DARK, points, 2)
        pygame.draw.line(surface, (255,255,255), (cx - r*0.5, cy - r*0.3), (cx + r*0.2, cy - r*0.5), 2)
    def _draw_rock(self, surface):
        r = self.radius
        # irregular polygon
        pts = []
        n = 7
        for i in range(n):
            ang = math.tau * i / n + self.wobble
            rad = r * (0.85 + 0.15 * math.sin(self.wobble * 3 + i * 1.7))
            pts.append((self.x + math.cos(ang) * rad, self.y + math.sin(ang) * rad))
        pygame.draw.polygon(surface, COLOR_ROCK, pts)
        pygame.draw.polygon(surface, COLOR_ROCK_DARK, pts, 2)
    def _draw_bone(self, surface):
        # a bone: shaft with two knobs at each end, slightly rotated
        ang = self.wobble * 0.3
        dx, dy = math.cos(ang), math.sin(ang)
        length = self.radius * 1.8
        x1, y1 = self.x - dx * length, self.y - dy * length
        x2, y2 = self.x + dx * length, self.y + dy * length
        pygame.draw.line(surface, COLOR_BONE, (x1, y1), (x2, y2), 6)
        k = self.radius * 0.55
        for (ex, ey) in ((x1, y1), (x2, y2)):
            pygame.draw.circle(surface, COLOR_BONE, (int(ex - dy * k), int(ey + dx * k)), int(k))
            pygame.draw.circle(surface, COLOR_BONE, (int(ex + dy * k), int(ey - dx * k)), int(k))
    def _draw_tnt(self, surface):
        r = self.radius
        rect = pygame.Rect(int(self.x - r), int(self.y - r * 0.8), int(r * 2), int(r * 1.6))
        pygame.draw.rect(surface, COLOR_TNT, rect, border_radius=3)
        pygame.draw.rect(surface, COLOR_TNT_DARK, rect, 2, border_radius=3)
        # fuse
        pygame.draw.line(surface, (120, 80, 40), (self.x, rect.top), (self.x + 6, rect.top - 8), 3)
        # label
        font = pygame.font.SysFont("arial", 12, bold=True)
        text = font.render("TNT", True, (255, 230, 120))
        surface.blit(text, text.get_rect(center=(self.x, self.y)))