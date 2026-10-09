'''
ui.py
HUD rendering and floating text effects.
'''
import pygame
from settings import (HUD_HEIGHT, HUD_BG, WHITE, BLACK, GREEN, RED, YELLOW,
                      GREY, SCREEN_WIDTH)
class FloatingText:
    def __init__(self, text, pos, color=WHITE, duration=1.2, rise=40, size=28):
        self.text = text
        self.pos = (float(pos[0]), float(pos[1]))
        self.color = color
        self.duration = duration
        self.rise = rise
        self.life = duration
        self.font = pygame.font.Font(None, size)
        self.surface = self.font.render(str(text), True, color)
    def update(self, dt):
        self.life -= dt
        self.pos = (self.pos[0], self.pos[1] - self.rise * dt)
    @property
    def dead(self):
        return self.life <= 0
    def draw(self, surface):
        if self.life <= 0:
            return
        s = self.surface.copy()
        alpha = max(0, int(255 * (self.life / self.duration)))
        s.set_alpha(alpha)
        rect = s.get_rect(center=(int(self.pos[0]), int(self.pos[1])))
        surface.blit(s, rect)