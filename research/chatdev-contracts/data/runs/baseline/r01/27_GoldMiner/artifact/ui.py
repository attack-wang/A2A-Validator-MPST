"""HUD, floating texts and full-screen messages."""
import math
import pygame
from settings import *
class FloatingText:
    """Short-lived rising text used for scores and effects."""
    def __init__(self, text, pos, color=WHITE, life=1.2):
        self.text = text
        self.x, self.y = pos
        self.color = color
        self.life = life
        self.max_life = life
    def update(self, dt):
        self.life -= dt
        self.y -= 30 * dt
    @property
    def alive(self):
        return self.life > 0
    def draw(self, surface, font):
        if self.life <= 0:
            return
        alpha = max(0, min(255, int(255 * self.life / self.max_life)))
        img = font.render(self.text, True, self.color)
        img.set_alpha(alpha)
        rect = img.get_rect(center=(int(self.x), int(self.y)))
        surface.blit(img, rect)
class HUD:
    """Draws score, level, timer, target and a claw position readout."""
    def __init__(self):
        self.font = pygame.font.SysFont("arial", 22, bold=True)
        self.big = pygame.font.SysFont("arial", 48, bold=True)
        self.small = pygame.font.SysFont("arial", 16)
    def draw(self, surface, level, level_score, target, total_score, time_left, claw):
        # top bar
        pygame.draw.rect(surface, UI_BG, (0, 0, WIDTH, GROUND_Y - 12))
        ...