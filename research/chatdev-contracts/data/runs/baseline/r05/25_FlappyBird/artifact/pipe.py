'''
Pipe obstacle: movement, gap geometry, collision, and rendering.
'''
import pygame
import settings
class Pipe:
    """A single pipe pair with a vertical gap the bird must fly through."""
    def __init__(self, x, gap_center, gap_size, speed):
        self.x = float(x)
        self.gap_center = float(gap_center)
        self.gap_size = float(gap_size)
        self.speed = float(speed)
        self.scored = False
        self._build_rects()
    def _build_rects(self):
        """Compute the top and bottom pipe rectangles from the gap geometry."""
        w = settings.PIPE_WIDTH
        ground_top = settings.SCREEN_HEIGHT - settings.GROUND_HEIGHT
        # Clamp the gap inside the playfield so rect heights never go negative.
        gap_top = max(0.0, self.gap_center - self.gap_size / 2.0)
        gap_bottom = min(float(ground_top), self.gap_center + self.gap_size / 2.0)
        self.top_rect = pygame.Rect(int(self.x), 0, w, int(gap_top))
        self.bottom_rect = pygame.Rect(int(self.x), int(gap_bottom), w, max(0, int(ground_top - gap_bottom)))
    def update(self, dt):
        """Move the pipe leftward."""
        self.x -= self.speed * dt
        self._build_rects()
    def offscreen(self):
        """True when the pipe has fully scrolled past the left edge."""
        return self.x + settings.PIPE_WIDTH < -10
    def collides(self, bird_rect):
        """True if the bird rectangle overlaps either pipe body."""
        return bird_rect.colliderect(self.top_rect) or bird_rect.colliderect(self.bottom_rect)
    def has_passed(self, bird_x):
        """True when the bird's center has cleared the pipe's right edge."""
        return not self.scored and bird_x > self.x + settings.PIPE_WIDTH
    def mark_scored(self):
        """Flag this pipe so it cannot be scored again."""
        self.scored = True
    def draw(self, surface):
        """Render both pipe halves with caps and shading."""
        self._draw_half(surface, self.top_rect, cap_bottom=True)
        self._draw_half(surface, self.bottom_rect, cap_bottom=False)
    def _draw_half(self, surface, rect, cap_bottom):
        """Draw one pipe half: body, highlight stripe, and end cap."""
        if rect.height <= 0:
            return
        pygame.draw.rect(surface, settings.PIPE_BODY, rect)
        # Shading stripe
        stripe = pygame.Rect(rect.x + 6, rect.y, 10, rect.height)
        pygame.draw.rect(surface, settings.PIPE_HIGHLIGHT, stripe)
        pygame.draw.rect(surface, settings.PIPE_EDGE, rect, 3)
        # Cap (the wider lip at the gap edge)
        cap_rect = pygame.Rect(rect.x - 4, 0, rect.width + 8, settings.PIPE_CAP_HEIGHT)
        if cap_bottom:
            cap_rect.bottom = rect.bottom
        else:
            cap_rect.top = rect.top
        pygame.draw.rect(surface, settings.PIPE_BODY, cap_rect)
        pygame.draw.rect(surface, settings.PIPE_EDGE, cap_rect, 3)