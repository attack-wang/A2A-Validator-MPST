'''Pipe obstacle: movement, collision, scoring, and rendering.'''
import pygame
from settings import (SCREEN_HEIGHT, PIPE_WIDTH, PIPE_CAP_HEIGHT, PIPE_CAP_OVERHANG)
from assets import create_pipe_body, create_pipe_cap
class Pipe:
    """A single pipe pair (top and bottom) with a vertical gap."""
    def __init__(self, x, gap_center_y, gap_size, speed):
        """Position the pipe and pre-render its body/cap surfaces."""
        self.x = float(x)
        self.gap_center = gap_center_y
        self.gap_size = gap_size
        self.speed = speed
        self.scored = False
        # geometry of the gap edges
        self.top_height = int(gap_center_y - gap_size / 2)   # bottom edge of top pipe
        self.bottom_y = int(gap_center_y + gap_size / 2)     # top edge of bottom pipe
        # pre-render stretched body segments and caps once
        top_body_h = max(1, self.top_height - PIPE_CAP_HEIGHT)
        bottom_body_h = max(1, SCREEN_HEIGHT - self.bottom_y - PIPE_CAP_HEIGHT)
        self.top_body = pygame.transform.scale(
            create_pipe_body(PIPE_WIDTH, 32), (PIPE_WIDTH, top_body_h))
        self.bottom_body = pygame.transform.scale(
            create_pipe_body(PIPE_WIDTH, 32), (PIPE_WIDTH, bottom_body_h))
        self.cap = create_pipe_cap(PIPE_WIDTH + PIPE_CAP_OVERHANG * 2, PIPE_CAP_HEIGHT)
    def update(self):
        """Scroll the pipe leftward at its current speed."""
        self.x -= self.speed
    def offscreen(self):
        """Return True once the pipe has fully scrolled past the left edge."""
        return self.x + PIPE_WIDTH + PIPE_CAP_OVERHANG < 0
    def get_gap_rect(self):
        """Return the rect of the vertical gap opening (for reference/debug)."""
        return pygame.Rect(int(self.x), self.top_height, PIPE_WIDTH,
                           self.bottom_y - self.top_height)
    def collides(self, rect):
        """Return True if the given rect hits either pipe body."""
        top_rect = pygame.Rect(int(self.x), 0, PIPE_WIDTH, self.top_height)
        bottom_rect = pygame.Rect(int(self.x), self.bottom_y, PIPE_WIDTH,
                                  SCREEN_HEIGHT - self.bottom_y)
        return rect.colliderect(top_rect) or rect.colliderect(bottom_rect)
    def has_passed(self, bird_x):
        """Return True the first time the bird's x clears the pipe's right edge."""
        if not self.scored and self.x + PIPE_WIDTH < bird_x:
            self.scored = True
            return True
        return False
    def draw(self, surface):
        """Blit pre-rendered top/bottom bodies and their caps."""
        cap_x = int(self.x) - PIPE_CAP_OVERHANG
        # top pipe
        surface.blit(self.top_body, (int(self.x), 0))
        surface.blit(self.cap, (cap_x, self.top_height - PIPE_CAP_HEIGHT))
        # bottom pipe
        surface.blit(self.cap, (cap_x, self.bottom_y))
        surface.blit(self.bottom_body, (int(self.x), self.bottom_y + PIPE_CAP_HEIGHT))