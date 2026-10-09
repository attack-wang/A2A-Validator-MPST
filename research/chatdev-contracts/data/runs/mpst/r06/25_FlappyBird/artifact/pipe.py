'''
pipe.py
Pipe obstacle: a vertical pair with a random gap, movement, collision
and rendering (procedurally drawn, no external assets).
'''
import pygame
from settings import (
    SCREEN_HEIGHT, GROUND_HEIGHT,
    PIPE_WIDTH, PIPE_CAP_HEIGHT, PIPE_CAP_OVERHANG,
    PIPE_GREEN, PIPE_DARK, PIPE_LIGHT,
)
class Pipe:
    """A single pipe pair (top + bottom) with a vertical gap."""
    def __init__(self, x, gap_center, gap_size):
        self.x = float(x)
        self.gap_center = gap_center
        self.gap_size = gap_size
        self.passed = False
        gap_top = gap_center - gap_size // 2
        gap_bottom = gap_center + gap_size // 2
        self.top_rect = pygame.Rect(int(x), 0, PIPE_WIDTH, gap_top)
        self.bottom_rect = pygame.Rect(
            int(x), gap_bottom, PIPE_WIDTH,
            SCREEN_HEIGHT - GROUND_HEIGHT - gap_bottom,
        )
    # ------------------------------------------------------------------ #
    def update(self, speed):
        """Scroll the pipe leftwards."""
        self.x -= speed
        self.top_rect.x = int(self.x)
        self.bottom_rect.x = int(self.x)
    def offscreen(self):
        """True once the pipe has fully left the screen."""
        return self.x + PIPE_WIDTH < 0
    def collides(self, rect):
        """Rect-based collision against either half of the pipe."""
        return self.top_rect.colliderect(rect) or self.bottom_rect.colliderect(rect)
    # ------------------------------------------------------------------ #
    def _draw_pipe(self, surface, rect, cap_y):
        """Draw one pipe body plus its wider cap lip."""
        # Body
        pygame.draw.rect(surface, PIPE_GREEN, rect)
        # Highlight stripe for a bit of depth
        pygame.draw.rect(surface, PIPE_LIGHT, (rect.x + 6, rect.y, 10, rect.height))
        # Outline
        pygame.draw.rect(surface, PIPE_DARK, rect, 2)
        # Cap (lip) at the gap edge
        cap = pygame.Rect(
            rect.x - PIPE_CAP_OVERHANG,
            cap_y,
            PIPE_WIDTH + PIPE_CAP_OVERHANG * 2,
            PIPE_CAP_HEIGHT,
        )
        pygame.draw.rect(surface, PIPE_GREEN, cap)
        pygame.draw.rect(surface, PIPE_LIGHT, (cap.x + 5, cap.y + 3, 10, PIPE_CAP_HEIGHT - 6))
        pygame.draw.rect(surface, PIPE_DARK, cap, 2)
    def draw(self, surface):
        """Render the full pipe pair."""
        # Top pipe: body from screen top, cap at its bottom edge
        self._draw_pipe(surface, self.top_rect, self.top_rect.bottom - PIPE_CAP_HEIGHT)
        # Bottom pipe: cap at its top edge
        self._draw_pipe(surface, self.bottom_rect, self.bottom_rect.top)