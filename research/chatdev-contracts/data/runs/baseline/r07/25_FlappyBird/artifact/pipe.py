'''
Pipe module: defines the pipe obstacles with a vertical gap.
'''
import random
import pygame
from settings import *
class Pipe:
    """A pair of vertical pipes with a random gap the bird must pass through."""
    def __init__(self, x, gap_center, gap_size):
        self.x = x
        self.gap_center = gap_center
        self.gap_size = gap_size
        self.width = PIPE_WIDTH
        self.scored = False
        self.top_height = gap_center - gap_size // 2
        self.bottom_y = gap_center + gap_size // 2
    @property
    def top_rect(self):
        return pygame.Rect(self.x, 0, self.width, self.top_height)
    @property
    def bottom_rect(self):
        h = max(0, SCREEN_HEIGHT - GROUND_HEIGHT - self.bottom_y)
        return pygame.Rect(self.x, self.bottom_y, self.width, h)
    def update(self, speed):
        self.x -= speed
    def offscreen(self):
        return self.x + self.width < -10
    def collides(self, rect):
        return rect.colliderect(self.top_rect) or rect.colliderect(self.bottom_rect)
    def has_passed(self, bird_x):
        return not self.scored and self.x + self.width < bird_x
    def _draw_pipe_body(self, surface, rect, cap_at_bottom):
        """Draw one pipe column: body gradient + highlight + cap lip."""
        pygame.draw.rect(surface, PIPE_GREEN, rect)
        # light highlight stripe
        pygame.draw.rect(surface, PIPE_LIGHT,
                         (rect.x + 6, rect.y, 10, rect.h))
        # dark shading stripe
        pygame.draw.rect(surface, PIPE_DARK,
                         (rect.x + rect.w - 12, rect.y, 8, rect.h))
        pygame.draw.rect(surface, PIPE_DARK, rect, 2)
        # cap lip
        cap = pygame.Rect(rect.x - PIPE_CAP_OVERHANG, 0,
                          rect.w + PIPE_CAP_OVERHANG * 2, PIPE_CAP_H)
        if cap_at_bottom:
            cap.bottom = rect.bottom
        else:
            cap.top = rect.top
        pygame.draw.rect(surface, PIPE_GREEN, cap)
        pygame.draw.rect(surface, PIPE_LIGHT, (cap.x + 4, cap.y + 3, 10, cap.h - 6))
        pygame.draw.rect(surface, PIPE_DARK, cap, 2)
    def draw(self, surface):
        """Draw top pipe (cap at its bottom) and bottom pipe (cap at its top)."""
        top = self.top_rect
        bottom = self.bottom_rect
        if top.h > 0:
            self._draw_pipe_body(surface, top, cap_at_bottom=True)
        if bottom.h > 0:
            self._draw_pipe_body(surface, bottom, cap_at_bottom=False)