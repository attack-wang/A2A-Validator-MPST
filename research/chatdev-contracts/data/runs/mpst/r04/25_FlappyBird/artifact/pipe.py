'''
pipe.py
Defines the Pipe class (a single obstacle with a random vertical gap)
and a module-level image cache so the pipe artwork is built only once.
'''
import pygame
import settings
_IMAGE_CACHE = None
_CAP_HEIGHT = 26
def _get_images():
    """Build (or return the cached) pipe body and cap surfaces."""
    global _IMAGE_CACHE
    if _IMAGE_CACHE is None:
        body = pygame.Surface((settings.PIPE_WIDTH, settings.SKY_HEIGHT), pygame.SRCALPHA)
        body.fill(settings.PIPE_GREEN)
        # light stripe on the left, dark shading on the right
        pygame.draw.rect(body, settings.PIPE_LIGHT, (6, 0, 10, body.get_height()))
        pygame.draw.rect(body, settings.PIPE_DARK,
                         (settings.PIPE_WIDTH - 10, 0, 8, body.get_height()))
        pygame.draw.rect(body, settings.PIPE_OUTLINE,
                         (0, 0, settings.PIPE_WIDTH, body.get_height()), 2)
        cap = pygame.Surface((settings.PIPE_WIDTH + 8, _CAP_HEIGHT), pygame.SRCALPHA)
        cap.fill(settings.PIPE_GREEN)
        pygame.draw.rect(cap, settings.PIPE_LIGHT, (6, 3, 10, _CAP_HEIGHT - 6))
        pygame.draw.rect(cap, settings.PIPE_DARK,
                         (cap.get_width() - 12, 3, 8, _CAP_HEIGHT - 6))
        pygame.draw.rect(cap, settings.PIPE_OUTLINE, (0, 0, cap.get_width(), _CAP_HEIGHT), 2)
        _IMAGE_CACHE = (body, cap, _CAP_HEIGHT)
    return _IMAGE_CACHE
class Pipe:
    """One pipe pair: a top pipe, a bottom pipe and the gap between them."""
    def __init__(self, x, gap_center, gap_size):
        self.x = float(x)
        self.gap_center = gap_center
        self.gap_size = gap_size
        self.gap_top = gap_center - gap_size / 2.0
        self.gap_bottom = gap_center + gap_size / 2.0
        self.scored = False
        self.body, self.cap, self.cap_height = _get_images()
    # ------------------------------------------------------------- update
    def update(self, dt, speed):
        """Scroll the pipe leftwards at the current game speed."""
        self.x -= speed * dt
    def is_offscreen(self):
        """True once the pipe has fully left the left edge."""
        return self.x + settings.PIPE_WIDTH < -10
    # ---------------------------------------------------------- collision
    def get_rects(self):
        """Collision rectangles for the top and bottom pipe sections."""
        top_rect = pygame.Rect(int(self.x), 0,
                               settings.PIPE_WIDTH, int(self.gap_top))
        bottom_rect = pygame.Rect(int(self.x), int(self.gap_bottom),
                                  settings.PIPE_WIDTH,
                                  settings.SKY_HEIGHT - int(self.gap_bottom))
        return top_rect, bottom_rect
    # -------------------------------------------------------------- draw
    def draw(self, surface):
        """Blit the top and bottom pipe sections with their caps."""
        x = int(self.x)
        gap_top = int(self.gap_top)
        gap_bottom = int(self.gap_bottom)
        # top pipe body
        if gap_top - self.cap_height > 0:
            surface.blit(self.body, (x, 0),
                         area=pygame.Rect(0, 0, settings.PIPE_WIDTH, gap_top - self.cap_height))
        surface.blit(self.cap, (x - 4, gap_top - self.cap_height))
        # bottom pipe body
        bottom_h = settings.SKY_HEIGHT - gap_bottom - self.cap_height
        if bottom_h > 0:
            surface.blit(self.body, (x, gap_bottom + self.cap_height),
                         area=pygame.Rect(0, 0, settings.PIPE_WIDTH, bottom_h))
        surface.blit(self.cap, (x - 4, gap_bottom))