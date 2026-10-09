"""Pipe entity: random gap generation, scrolling, collision and rendering."""
import random
import pygame
import settings
import utils
class Pipe:
    """A vertical pipe pair with a randomly placed gap the bird must fly through."""
    def __init__(self, x, score):
        """Spawn a pipe at horizontal position x; the gap shrinks as score grows."""
        self.x = float(x)
        self.width = settings.PIPE_WIDTH
        self.passed = False  # becomes True once the bird has scored on this pipe
        # Gap size depends on the current score (difficulty progression).
        gap_size = settings.get_gap_size(score)
        ground_top = settings.SCREEN_HEIGHT - settings.GROUND_HEIGHT
        # Keep the whole gap (plus a safety margin) between screen top and ground.
        lowest_center = ground_top - settings.GAP_MARGIN - gap_size / 2.0
        highest_center = settings.GAP_MARGIN + gap_size / 2.0
        gap_center = random.uniform(highest_center, lowest_center)
        self.gap_top = gap_center - gap_size / 2.0
        self.gap_bottom = gap_center + gap_size / 2.0
        self._refresh_rects()
    def _refresh_rects(self):
        """Recompute collision and cap rectangles from the current position."""
        ground_top = settings.SCREEN_HEIGHT - settings.GROUND_HEIGHT
        # Column rects used for collision (decorative caps overhang slightly but
        # are excluded from collision so hits stay fair for the player).
        self.top_rect = pygame.Rect(int(self.x), 0,
                                    self.width, int(self.gap_top))
        self.bottom_rect = pygame.Rect(int(self.x), int(self.gap_bottom),
                                       self.width,
                                       ground_top - int(self.gap_bottom))
        # Wider decorative caps at the gap edges.
        cap_width = self.width + 2 * settings.PIPE_CAP_OVERHANG
        self.cap_top_rect = pygame.Rect(int(self.x) - settings.PIPE_CAP_OVERHANG,
                                        int(self.gap_top) - settings.PIPE_CAP_HEIGHT,
                                        cap_width, settings.PIPE_CAP_HEIGHT)
        self.cap_bottom_rect = pygame.Rect(int(self.x) - settings.PIPE_CAP_OVERHANG,
                                           int(self.gap_bottom),
                                           cap_width, settings.PIPE_CAP_HEIGHT)
    def update(self, dt, speed):
        """Scroll the pipe leftwards at the current game speed."""
        self.x -= speed * dt
        self._refresh_rects()
    def offscreen(self):
        """Return True once the pipe (including its caps) has left the screen."""
        return self.x + self.width + settings.PIPE_CAP_OVERHANG < 0
    def collide(self, bird_rect):
        """Return True when the bird rect intersects either pipe column."""
        return (bird_rect.colliderect(self.top_rect)
                or bird_rect.colliderect(self.bottom_rect))
    def has_passed(self, bird_x):
        """Return True when the bird's x has cleared this pipe (not yet scored)."""
        return not self.passed and bird_x > self.x + self.width
    def mark_passed(self):
        """Flag this pipe as scored so it cannot be counted twice."""
        self.passed = True
    def draw(self, surface):
        """Draw both pipe columns and their caps."""
        utils.draw_pipe_column(surface, self.top_rect)
        utils.draw_pipe_column(surface, self.bottom_rect)
        utils.draw_pipe_cap(surface, self.cap_top_rect)
        utils.draw_pipe_cap(surface, self.cap_bottom_rect)