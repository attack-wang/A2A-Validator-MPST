'''
pipe.py
Pipe obstacle: random gap placement, movement, collision and rendering.
Each pipe pair is generated with a random vertical gap position.
'''
import random
import pygame
from settings import (
    SCREEN_HEIGHT, GROUND_HEIGHT, PIPE_WIDTH, PIPE_CAP_HEIGHT,
    PIPE_CAP_OVERHANG, PIPE_MARGIN,
    PIPE_BODY, PIPE_DARK, PIPE_LIGHT, PIPE_CAP, OUTLINE,
)
class Pipe:
    """A pair of pipes with a vertical gap the bird must fly through."""
    def __init__(self, x, gap_size):
        self.x = float(x)
        self.gap_size = int(gap_size)
        top_limit = PIPE_MARGIN + self.gap_size // 2
        bottom_limit = SCREEN_HEIGHT - GROUND_HEIGHT - PIPE_MARGIN - self.gap_size // 2
        if bottom_limit < top_limit:  # safety for extreme gaps
            top_limit = bottom_limit = SCREEN_HEIGHT // 2
        self.gap_center = random.randint(top_limit, bottom_limit)
        self.scored = False
        self.top_rect = pygame.Rect(int(self.x), 0, PIPE_WIDTH, self.gap_top)
        self.bottom_rect = pygame.Rect(
            int(self.x), self.gap_bottom, PIPE_WIDTH,
            SCREEN_HEIGHT - GROUND_HEIGHT - self.gap_bottom
        )
    @property
    def gap_top(self):
        return self.gap_center - self.gap_size // 2
    @property
    def gap_bottom(self):
        return self.gap_center + self.gap_size // 2
    def update(self, speed):
        self.x -= speed
        self.top_rect.x = int(self.x)
        self.bottom_rect.x = int(self.x)
    def offscreen(self):
        return self.x + PIPE_WIDTH < 0
    def collides(self, rect):
        return self.top_rect.colliderect(rect) or self.bottom_rect.colliderect(rect)
    def draw(self, surface):
        self._draw_column(surface, self.top_rect, cap_bottom=True)
        self._draw_column(surface, self.bottom_rect, cap_bottom=False)
    def _draw_column(self, surface, rect, cap_bottom):
        # main body
        pygame.draw.rect(surface, PIPE_BODY, rect)
        # shading strips
        light_strip = pygame.Rect(rect.x + 4, rect.y, 10, rect.height)
        pygame.draw.rect(surface, PIPE_LIGHT, light_strip)
        dark_strip = pygame.Rect(rect.right - 14, rect.y, 10, rect.height)
        pygame.draw.rect(surface, PIPE_DARK, dark_strip)
        # outline
        pygame.draw.rect(surface, OUTLINE, rect, 2)
        # cap (slightly wider than the body)
        cap_rect = pygame.Rect(
            rect.x - PIPE_CAP_OVERHANG,
            rect.y if cap_bottom else rect.bottom - PIPE_CAP_HEIGHT,
            PIPE_WIDTH + PIPE_CAP_OVERHANG * 2,
            PIPE_CAP_HEIGHT,
        )
        pygame.draw.rect(surface, PIPE_CAP, cap_rect)
        pygame.draw.rect(surface, OUTLINE, cap_rect, 2)