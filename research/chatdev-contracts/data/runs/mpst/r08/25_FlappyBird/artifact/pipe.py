'''
Pipe obstacle: rendering, movement and collision.
'''
import pygame
import settings
class Pipe:
    """A single pipe pair (top and bottom) with a vertical gap."""
    def __init__(self, x, gap_center, gap_size, speed):
        self.x = float(x)
        self.gap_center = float(gap_center)
        self.gap_size = float(gap_size)
        self.speed = speed
        self.scored = False
    @property
    def gap_top(self):
        """Y coordinate of the lower edge of the top pipe."""
        return self.gap_center - self.gap_size / 2
    @property
    def gap_bottom(self):
        """Y coordinate of the upper edge of the bottom pipe."""
        return self.gap_center + self.gap_size / 2
    def update(self, dt, speed):
        """Move the pipe left by the current world speed."""
        self.x -= speed * dt
    def is_offscreen(self):
        """True once the pipe has fully left the left edge."""
        return self.x + settings.PIPE_WIDTH < -10
    def collides(self, rect):
        """Rect-based collision against both pipe halves."""
        # Extend the top rect above the screen so the bird cannot
        # fly over the pipes near the ceiling.
        top = pygame.Rect(int(self.x), -100, settings.PIPE_WIDTH, int(self.gap_top) + 100)
        ground_top = settings.SCREEN_HEIGHT - settings.GROUND_HEIGHT
        bottom = pygame.Rect(int(self.x), int(self.gap_bottom), settings.PIPE_WIDTH, int(ground_top - self.gap_bottom))
        return rect.colliderect(top) or rect.colliderect(bottom)
    def has_passed(self, bird_x):
        """Score once the pipe's right edge is behind the bird."""
        if not self.scored and self.x + settings.PIPE_WIDTH < bird_x:
            self.scored = True
            return True
        return False
    def draw(self, screen):
        """Render both pipe halves with caps, highlight and outline."""
        x = int(self.x)
        w = settings.PIPE_WIDTH
        cap_h = settings.PIPE_CAP_HEIGHT
        over = settings.PIPE_CAP_OVERHANG
        ground_top = settings.SCREEN_HEIGHT - settings.GROUND_HEIGHT
        top_h = int(self.gap_top)
        bottom_y = int(self.gap_bottom)
        bottom_h = ground_top - bottom_y
        if top_h > 0:
            body = pygame.Rect(x, -10, w, top_h + 10)
            pygame.draw.rect(screen, settings.PIPE_BODY, body)
            pygame.draw.rect(screen, settings.PIPE_HIGHLIGHT, (x + 5, -10, 9, top_h + 10))
            pygame.draw.rect(screen, settings.PIPE_EDGE, body, 2)
            cap = pygame.Rect(x - over, top_h - cap_h, w + over * 2, cap_h)
            pygame.draw.rect(screen, settings.PIPE_BODY, cap)
            pygame.draw.rect(screen, settings.PIPE_HIGHLIGHT, (x - over + 4, top_h - cap_h + 3, 9, cap_h - 6))
            pygame.draw.rect(screen, settings.PIPE_EDGE, cap, 2)
        if bottom_h > 0:
            body = pygame.Rect(x, bottom_y, w, bottom_h)
            pygame.draw.rect(screen, settings.PIPE_BODY, body)
            pygame.draw.rect(screen, settings.PIPE_HIGHLIGHT, (x + 5, bottom_y, 9, bottom_h))
            pygame.draw.rect(screen, settings.PIPE_EDGE, body, 2)
            cap = pygame.Rect(x - over, bottom_y, w + over * 2, cap_h)
            pygame.draw.rect(screen, settings.PIPE_BODY, cap)
            pygame.draw.rect(screen, settings.PIPE_HIGHLIGHT, (x - over + 4, bottom_y + 3, 9, cap_h - 6))
            pygame.draw.rect(screen, settings.PIPE_EDGE, cap, 2)