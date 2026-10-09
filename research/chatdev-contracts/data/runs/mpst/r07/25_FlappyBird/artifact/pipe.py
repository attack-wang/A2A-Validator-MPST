"""
pipe.py
The Pipe obstacle: a vertical pair of green pipes with a random gap.
Each Pipe knows how to move, collide with the bird, report when it has
been passed (for scoring) and render itself with caps and shading.
"""
import random
import pygame
import settings
class Pipe:
    """A single pipe pair (top pipe, gap, bottom pipe) scrolling left."""
    def __init__(self, x, gap_center_y, gap_height):
        self.x = float(x)
        self.gap_center_y = float(gap_center_y)
        self.gap_height = int(gap_height)
        self.width = settings.PIPE_WIDTH
        self.passed = False  # becomes True once the bird has scored on it
    # ------------------------------------------------------------------ geometry
    @property
    def gap_top(self):
        return self.gap_center_y - self.gap_height / 2
    @property
    def gap_bottom(self):
        return self.gap_center_y + self.gap_height / 2
    def _body_rects(self):
        ground_y = settings.SCREEN_HEIGHT - settings.GROUND_HEIGHT
        top = pygame.Rect(int(self.x), 0, self.width, int(self.gap_top))
        bottom = pygame.Rect(int(self.x), int(self.gap_bottom), self.width,
                             int(ground_y - self.gap_bottom))
        return top, bottom
    def _cap_rects(self):
        cap_w = self.width + settings.PIPE_CAP_OVERHANG * 2
        cap_x = int(self.x) - settings.PIPE_CAP_OVERHANG
        top_cap = pygame.Rect(cap_x, int(self.gap_top) - settings.PIPE_CAP_HEIGHT,
                              cap_w, settings.PIPE_CAP_HEIGHT)
        bottom_cap = pygame.Rect(cap_x, int(self.gap_bottom), cap_w,
                                 settings.PIPE_CAP_HEIGHT)
        return top_cap, bottom_cap
    # ------------------------------------------------------------------ behaviour
    def update(self, speed):
        self.x -= speed
    def is_offscreen(self):
        return self.x + self.width < -settings.PIPE_CAP_OVERHANG
    def has_passed(self, bird_x):
        """True the moment the bird's centre crosses the pipe's centre."""
        return not self.passed and bird_x > self.x + self.width / 2
    def mark_passed(self):
        self.passed = True
    def collides(self, rect):
        """Rect-based collision against both pipe bodies and both caps."""
        top, bottom = self._body_rects()
        top_cap, bottom_cap = self._cap_rects()
        for obstacle in (top, bottom, top_cap, bottom_cap):
            if rect.colliderect(obstacle):
                return True
        return False
    # ------------------------------------------------------------------ drawing
    def _draw_column(self, surface, body, cap):
        """Render one pipe column (body + cap) with simple shading."""
        # Body
        pygame.draw.rect(surface, settings.PIPE_BODY, body)
        # Light stripe on the left, dark stripe on the right -> cheap 3D look
        pygame.draw.rect(surface, settings.PIPE_BODY_LIGHT,
                         (body.x + 6, body.y, 12, body.h))
        pygame.draw.rect(surface, settings.PIPE_BODY_DARK,
                         (body.right - 12, body.y, 12, body.h))
        pygame.draw.rect(surface, settings.PIPE_OUTLINE, body, 2)
        # Cap
        pygame.draw.rect(surface, settings.PIPE_BODY, cap)
        pygame.draw.rect(surface, settings.PIPE_BODY_LIGHT,
                         (cap.x + 6, cap.y, 12, cap.h))
        pygame.draw.rect(surface, settings.PIPE_BODY_DARK,
                         (cap.right - 12, cap.y, 12, cap.h))
        pygame.draw.rect(surface, settings.PIPE_OUTLINE, cap, 2)
    def draw(self, surface):
        top, bottom = self._body_rects()
        top_cap, bottom_cap = self._cap_rects()
        self._draw_column(surface, top, top_cap)
        self._draw_column(surface, bottom, bottom_cap)