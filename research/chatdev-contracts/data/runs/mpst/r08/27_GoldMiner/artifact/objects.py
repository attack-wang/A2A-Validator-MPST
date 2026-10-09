'''Mineable objects for the Gold Miner game.'''
import math
import random
import pygame
from settings import (OBJECT_STATS, GOLD, GOLD_DARK, GRAY, GRAY_DARK,
                      CYAN, WHITE, BONE_WHITE, RED, BLACK, ORANGE)
_font_cache = {}
def _get_font(size):
    """Lazily create and cache pygame fonts for object labels."""
    if size not in _font_cache:
        _font_cache[size] = pygame.font.Font(None, size)
    return _font_cache[size]
class GameObject:
    """A single mineable item sitting in the dirt."""
    def __init__(self, kind, x, y):
        self.kind = kind
        stats = OBJECT_STATS[kind]
        self.x = x
        self.y = y
        self.radius = stats['radius']
        self.base_value = stats['value']
        self.weight = stats['weight']
        self.attached = False
        if kind == 'mystery':
            self.value = random.choice([50, 100, 200, 400, 800])
            self.weight = random.uniform(1.0, 4.0)
        else:
            self.value = self.base_value
    @property
    def reel_speed_factor(self):
        """Higher weight => slower reeling (divisor for retract speed)."""
        return self.weight
    def draw(self, surface):
        """Draw the object with a simple shape unique to its kind."""
        x, y, r = int(self.x), int(self.y), self.radius
        if self.kind in ('small_gold', 'medium_gold', 'large_gold'):
            pygame.draw.circle(surface, GOLD, (x, y), r)
            pygame.draw.circle(surface, GOLD_DARK, (x, y), r, 2)
            pygame.draw.circle(surface, WHITE, (x - r // 3, y - r // 3), max(2, r // 4))
        elif self.kind == 'diamond':
            pts = [(x, y - r), (x + r, y), (x, y + r), (x - r, y)]
            pygame.draw.polygon(surface, CYAN, pts)
            pygame.draw.polygon(surface, WHITE, pts, 2)
        elif self.kind in ('rock_small', 'rock_big'):
            pts = []
            for i in range(7):
                ang = math.radians(i * (360.0 / 7))
                rr = r * (0.85 + 0.15 * math.sin(i * 2.3 + x))
                pts.append((x + math.cos(ang) * rr, y + math.sin(ang) * rr))
            pygame.draw.polygon(surface, GRAY, pts)
            pygame.draw.polygon(surface, GRAY_DARK, pts, 2)
        elif self.kind == 'bone':
            thick = max(3, r // 3)
            pygame.draw.line(surface, BONE_WHITE, (x - r, y + r // 2), (x + r, y - r // 2), thick)
            pygame.draw.circle(surface, BONE_WHITE, (x - r, y + r // 2), thick)
            pygame.draw.circle(surface, BONE_WHITE, (x + r, y - r // 2), thick)
        elif self.kind == 'tnt':
            rect = pygame.Rect(x - r, y - r, 2 * r, 2 * r)
            pygame.draw.rect(surface, RED, rect)
            pygame.draw.rect(surface, BLACK, rect, 2)
            text = _get_font(20).render('TNT', True, WHITE)
            surface.blit(text, text.get_rect(center=(x, y)))
        else:  # mystery
            pygame.draw.circle(surface, ORANGE, (x, y), r)
            pygame.draw.circle(surface, BLACK, (x, y), r, 2)
            text = _get_font(24).render('?', True, BLACK)
            surface.blit(text, text.get_rect(center=(x, y)))