"""Transient visual effects: floating score text and explosion rings."""
import pygame
import config
_FONT = None
def _font():
    global _FONT
    if _FONT is None:
        pygame.font.init()
        _FONT = pygame.font.Font(None, 30)
    return _FONT
class FloatingText:
    def __init__(self, x, y, text, color, lifetime=1.0):
        self.x = x
        self.y = y
        self.text = text
        self.color = color
        self.lifetime = lifetime
        self.age = 0.0
    def update(self, dt):
        self.age += dt
        self.y -= 30 * dt
        return self.age < self.lifetime
    def draw(self, surface):
        alpha = max(0, int(255 * (1 - self.age / self.lifetime)))
        img = _font().render(self.text, True, self.color)
        img.set_alpha(alpha)
        surface.blit(img, (self.x - img.get_width() // 2, self.y - img.get_height() // 2))
class Explosion:
    def __init__(self, x, y, radius, lifetime=0.5):
        self.x = x
        self.y = y
        self.radius = radius
        self.lifetime = lifetime
        self.age = 0.0
    def update(self, dt):
        self.age += dt
        return self.age < self.lifetime
    def draw(self, surface):
        t = self.age / self.lifetime
        r = int(self.radius * (0.3 + 0.7 * t))
        alpha = int(255 * (1 - t))
        color = (255, 200, 80) if t < 0.5 else (255, 120, 40)
        temp = pygame.Surface((r * 2, r * 2), pygame.SRCALPHA)
        pygame.draw.circle(temp, (*color, alpha), (r, r), r)
        pygame.draw.circle(temp, (*color, min(255, alpha + 60)), (r, r), max(1, int(r * 0.7)))
        surface.blit(temp, (self.x - r, self.y - r))