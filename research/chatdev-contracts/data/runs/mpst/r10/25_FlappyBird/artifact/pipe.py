'''
pipe.py
The Pipe obstacle: a vertical pair of green columns with a randomly
placed gap. Handles movement, off-screen cleanup, scoring bookkeeping
and collision tests against the bird's rectangle.
'''
import random
import pygame
import settings
class Pipe:
    """One pipe pair (top column + bottom column) sharing a vertical gap."""
    def __init__(self, x, speed, gap_size, gap_top=None):
        """Build the pair; gap_top may be supplied for fair sequencing."""
        self.x = float(x)
        self.speed = float(speed)
        self.gap_size = int(gap_size)
        if gap_top is None:
            self.gap_top = self._random_gap_top()
        else:
            # Clamp a caller-supplied gap top into the legal band.
            lowest = (settings.SCREEN_HEIGHT - settings.GROUND_HEIGHT
                      - self.gap_size - settings.PIPE_MARGIN_BOTTOM)
            self.gap_top = max(settings.PIPE_MARGIN_TOP,
                               min(int(gap_top), lowest))
        self.gap_bottom = self.gap_top + self.gap_size
        self.scored = False
        ground_y = settings.SCREEN_HEIGHT - settings.GROUND_HEIGHT
        self.top_rect = pygame.Rect(int(self.x), 0,
                                    settings.PIPE_WIDTH, self.gap_top)
        self.bottom_rect = pygame.Rect(int(self.x), self.gap_bottom,
                                       settings.PIPE_WIDTH,
                                       ground_y - self.gap_bottom)