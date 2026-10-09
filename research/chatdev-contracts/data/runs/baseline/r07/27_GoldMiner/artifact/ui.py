'''HUD and screen rendering: score, goal progress, timer, claw readout, menus.'''
import math
import random
import pygame
from settings import *
class FloatingText:
    """Short-lived text popup that floats upward and fades out."""
    def __init__(self, x, y, text, color, lifetime=1.2):
        self.x = x
        self.y = y
        self.text = text
        self.color = color
        self.lifetime = lifetime
        self.age = 0.0
        self.font = pygame.font.SysFont('arial', 24, bold=True)
    def update(self, dt):
        self.age += dt
        self.y -= 30 * dt
        return self.age < self.lifetime
    def draw(self, surface):
        alpha = max(0, 1.0 - self.age / self.lifetime)
        surf = self.font.render(self.text, True, self.color)
        surf.set_alpha(int(255 * alpha))
        surface.blit(surf, surf.get_rect(center=(int(self.x), int(self.y))))
class UI:
    def __init__(self):
        self.font_big = pygame.font.SysFont('arial', 52, bold=True)
        self.font_med = pygame.font.SysFont('arial', 30, bold=True)
        self.font_small = pygame.font.SysFont('arial', 22)
        self.font_tiny = pygame.font.SysFont('arial', 18)
        # deterministic speckle pattern
        rng = random.Random(42)
        self.speckles = []
        for _ in range(120):
            x = rng.randint(0, SCREEN_WIDTH)
            y = rng.randint(FIELD_TOP, SCREEN_HEIGHT)
            r = rng.randint(1, 3)
            self.speckles.append((x, y, r))