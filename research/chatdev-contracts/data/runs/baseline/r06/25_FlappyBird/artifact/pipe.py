"""
pipe.py
Pipe entity: movement, collision, scoring bookkeeping and rendering.
Pipes do not own a speed; they are moved with the game's current
global scroll speed each frame so faster new pipes can never overtake
slower old ones.
"""
import pygame
from settings import (PIPE_WIDTH, PIPE_CAP_H, PIPE_CAP_OVERHANG,
                      HEIGHT, GROUND_HEIGHT,
                      PIPE_BODY, PIPE_DARK, PIPE_LIGHT)
class Pipe:
    """A single pipe pair (top + bottom) with a vertical gap."""
    def __init__(self, x, gap_center, gap_size):
        self.x = float(x)
        self.gap_center = float(gap_center)
        self.gap_size = float(gap_size)
        self.scored = False
        top_bottom = int(self.gap_center - self.gap_size / 2)
        bottom_top = int(self.gap_center + self.gap_size / 2)
        self.top_rect = pygame.Rect(int(x), 0, PIPE_WIDTH, top_bottom)
        self.bottom_rect = pygame.Rect(int(x), bottom_top, PIPE_WIDTH,
                                       HEIGHT - GROUND_HEIGHT - bottom_top)
    def update(self, dt, speed):
        """Move left at the caller-provided (current global) speed."""
        self.x -= speed * dt
        self.top_rect.x = int(self.x)
        self.bottom_rect.x = int(self.x)
    def offscreen(self):
        return self.x + PIPE_WIDTH < -10
    def collides(self, rect):
        return (self.top_rect.colliderect(rect)
                or self.bottom_rect.colliderect(rect))
    def has_passed(self, bird_x):
        return not self.scored and self.x + PIPE_WIDTH < bird_x
    def mark_scored(self):
        self.scored = True
    def draw(self, surface):
        """Render both pipe halves with caps, outline and highlight stripe."""
        # ---- top pipe -------------------------------------------------
        pygame.draw.rect(surface, PIPE_BODY, self.top_rect)
        pygame.draw.rect(surface, PIPE_LIGHT,
                         (self.top_rect.x + 6, self.top_rect.y, 10,
                          self.top_rect.height))
        pygame.draw.rect(surface, PIPE_DARK, self.top_rect, 2)
        cap = pygame.Rect(self.top_rect.x - PIPE_CAP_OVERHANG,
                          self.top_rect.bottom - PIPE_CAP_H,
                          PIPE_WIDTH + PIPE_CAP_OVERHANG * 2, PIPE_CAP_H)
        pygame.draw.rect(surface, PIPE_BODY, cap)
        pygame.draw.rect(surface, PIPE_DARK, cap, 2)
        # ---- bottom pipe ----------------------------------------------
        pygame.draw.rect(surface, PIPE_BODY, self.bottom_rect)
        pygame.draw.rect(surface, PIPE_LIGHT,
                         (self.bottom_rect.x + 6, self.bottom_rect.y, 10,
                          self.bottom_rect.height))
        pygame.draw.rect(surface, PIPE_DARK, self.bottom_rect, 2)
        cap = pygame.Rect(self.bottom_rect.x - PIPE_CAP_OVERHANG,
                          self.bottom_rect.y,
                          PIPE_WIDTH + PIPE_CAP_OVERHANG * 2, PIPE_CAP_H)
        pygame.draw.rect(surface, PIPE_BODY, cap)
        pygame.draw.rect(surface, PIPE_DARK, cap, 2)