"""Pipe obstacles with random gaps and difficulty-driven movement."""
import random
import pygame
import settings
class Pipe:
    """A single pipe pair (top and bottom) with a vertical gap."""
    def __init__(self, x, gap_center, gap_size, speed):
        self.x = float(x)
        self.gap_center = gap_center
        self.gap_size = gap_size
        self.speed = speed
        self.scored = False
        gap_top = gap_center - gap_size / 2
        gap_bottom = gap_center + gap_size / 2
        self.top_rect = pygame.Rect(int(x), 0, settings.PIPE_WIDTH, int(gap_top))
        self.bottom_rect = pygame.Rect(
            int(x), int(gap_bottom), settings.PIPE_WIDTH,
            settings.SCREEN_HEIGHT - settings.GROUND_HEIGHT - int(gap_bottom))
        self._cap_width = settings.PIPE_WIDTH + settings.PIPE_CAP_OVERHANG * 2
    def update(self, dt):
        """Move the pipe left and keep its collision rects in sync."""
        self.x -= self.speed * dt
        self.top_rect.x = int(self.x)
        self.bottom_rect.x = int(self.x)
    def draw(self, surface):
        """Draw the top and bottom pipe bodies with caps facing the gap."""
        self._draw_pipe_body(surface, self.top_rect, cap_at_bottom=True)
        self._draw_pipe_body(surface, self.bottom_rect, cap_at_top=True)
    def _draw_pipe_body(self, surface, rect, cap_at_top=False, cap_at_bottom=False):
        """Render one pipe column: body, highlight stripe, outline, and cap."""
        pygame.draw.rect(surface, settings.PIPE_BODY_COLOR, rect)
        stripe = pygame.Rect(rect.x + 6, rect.y, 10, rect.height)
        pygame.draw.rect(surface, settings.PIPE_LIGHT_COLOR, stripe)
        pygame.draw.rect(surface, settings.PIPE_DARK_COLOR, rect, 2)
        if cap_at_top:
            cap = pygame.Rect(rect.x - settings.PIPE_CAP_OVERHANG, rect.y - settings.PIPE_CAP_HEIGHT,
                              self._cap_width, settings.PIPE_CAP_HEIGHT)
            pygame.draw.rect(surface, settings.PIPE_CAP_COLOR, cap)
            pygame.draw.rect(surface, settings.PIPE_DARK_COLOR, cap, 2)
        if cap_at_bottom:
            cap = pygame.Rect(rect.x - settings.PIPE_CAP_OVERHANG, rect.bottom - settings.PIPE_CAP_HEIGHT,
                              self._cap_width, settings.PIPE_CAP_HEIGHT)
            pygame.draw.rect(surface, settings.PIPE_CAP_COLOR, cap)
            pygame.draw.rect(surface, settings.PIPE_DARK_COLOR, cap, 2)
    def collides_with(self, rect):
        """Return True if the given rect overlaps either pipe column."""
        return rect.colliderect(self.top_rect) or rect.colliderect(self.bottom_rect)
    def has_passed(self, bird_x):
        """Return True when the bird has cleared this pipe (for scoring)."""
        return not self.scored and (self.x + settings.PIPE_WIDTH) < bird_x
    def is_offscreen(self):
        """Return True once the pipe has fully scrolled off the left edge."""
        return self.x + self._cap_width < 0