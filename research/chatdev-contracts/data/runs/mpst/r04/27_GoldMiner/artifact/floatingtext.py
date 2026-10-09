"""Floating score/status text that rises and fades after events."""
import pygame
import settings
class FloatingText:
    """Text that floats upward and disappears after a short lifetime."""
    def __init__(self, x, y, text, color):
        self.x = x
        self.y = y
        self.text = text
        self.color = color
        self.life = 1.2
        self.max_life = 1.2
    def update(self, dt):
        self.y -= 40 * dt
        self.life -= dt
    @property
    def expired(self):
        return self.life <= 0
    def draw(self, surface, font):
        if self.expired:
            return
        alpha = max(0, int(255 * self.life / self.max_life))
        img = font.render(self.text, True, self.color)
        img.set_alpha(alpha)
        surface.blit(img, (int(self.x) - img.get_width() // 2, int(self.y)))