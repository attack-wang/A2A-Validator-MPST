"""Pipe pair entity: scrolling, gap generation support, collision and rendering."""
import pygame
import settings
class Pipe:
    """A single pipe pair with a vertical gap; scrolls left and detects collisions."""
    def __init__(self, x, gap_center_y, gap_size, speed):
        self.x = float(x)
        self.gap_center_y = gap_center_y
        self.gap_size = gap_size
        self.speed = speed
        self.passed = False
        ground_y = settings.SCREEN_HEIGHT - settings.GROUND_HEIGHT
        gap_top = max(gap_center_y - gap_size / 2, settings.PIPE_MARGIN)
        gap_bottom = min(gap_center_y + gap_size / 2, ground_y - settings.PIPE_MARGIN)
        self.top_rect = pygame.Rect(int(self.x), 0, settings.PIPE_WIDTH, int(gap_top))
        self.bottom_rect = pygame.Rect(int(self.x), int(gap_bottom),
                                       settings.PIPE_WIDTH, int(ground_y - gap_bottom))
    def update(self):
        """Scroll the pipe pair to the left."""
        self.x -= self.speed
        self.top_rect.x = int(self.x)
        self.bottom_rect.x = int(self.x)
    def collides(self, bird_rect):
        """True if the bird's bounding box hits either pipe half."""
        return bird_rect.colliderect(self.top_rect) or bird_rect.colliderect(self.bottom_rect)
    def has_passed(self, bird_x):
        """Score helper: returns True exactly once when the pipe clears the bird."""
        if not self.passed and self.x + settings.PIPE_WIDTH < bird_x:
            self.passed = True
            return True
        return False
    def offscreen(self):
        """True when the pipe has fully scrolled off the left edge."""
        return self.x + settings.PIPE_WIDTH < 0
    def draw(self, screen):
        """Render both pipe halves with caps and a subtle highlight."""
        for rect in (self.top_rect, self.bottom_rect):
            pygame.draw.rect(screen, settings.GREEN, rect)
            pygame.draw.rect(screen, settings.DARK_GREEN, rect, 3)
            pygame.draw.rect(screen, settings.LIGHT_GREEN,
                             (rect.x + 6, rect.y + 4, 8, max(rect.height - 8, 0)))
        for rect in (self.top_rect, self.bottom_rect):
            if rect.height <= 0:
                continue
            cap_y = rect.bottom - settings.PIPE_CAP_HEIGHT if rect is self.top_rect else rect.top
            cap_rect = pygame.Rect(rect.x - settings.PIPE_CAP_OVERHANG, cap_y,
                                   settings.PIPE_WIDTH + 2 * settings.PIPE_CAP_OVERHANG,
                                   settings.PIPE_CAP_HEIGHT)
            pygame.draw.rect(screen, settings.DARK_GREEN, cap_rect)
            pygame.draw.rect(screen, settings.BLACK, cap_rect, 2)