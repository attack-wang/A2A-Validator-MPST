"""Pipe entity: generation, movement, collision, and rendering."""
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
        self._compute_rects()
    def _compute_rects(self):
        """Compute the top and bottom pipe rectangles from the gap."""
        gap_top = self.gap_center - self.gap_size / 2
        gap_bottom = self.gap_center + self.gap_size / 2
        ground_top = settings.SCREEN_HEIGHT - settings.GROUND_HEIGHT
        self.top_rect = pygame.Rect(int(self.x), 0, settings.PIPE_WIDTH, int(gap_top))
        self.bottom_rect = pygame.Rect(
            int(self.x), int(gap_bottom),
            settings.PIPE_WIDTH, int(ground_top - gap_bottom),
        )
    def update(self, dt):
        """Move the pipe leftward and refresh its rectangles."""
        self.x -= self.speed * dt
        self._compute_rects()
    def is_offscreen(self):
        """True when the pipe has fully scrolled past the left edge."""
        return self.x + settings.PIPE_WIDTH < -settings.PIPE_CAP_OVERHANG
    def collides_with(self, hitbox):
        """Return True if the bird's hitbox intersects either pipe section."""
        return hitbox.colliderect(self.top_rect) or hitbox.colliderect(self.bottom_rect)
    def check_score(self, bird_center_x):
        """Award a point the first time the bird clears this pipe."""
        if not self.scored and self.x + settings.PIPE_WIDTH < bird_center_x:
            self.scored = True
            return True
        return False
    def draw(self, surface):
        """Render both pipe sections with caps and shading."""
        for rect, is_top in ((self.top_rect, True), (self.bottom_rect, False)):
            if rect.height <= 0:
                continue
            pygame.draw.rect(surface, settings.GREEN, rect)
            # lighter left edge for a subtle 3D look
            pygame.draw.rect(surface, settings.WHITE, (rect.x + 3, rect.y, 6, rect.height))
            pygame.draw.rect(surface, settings.DARK_GREEN, rect, 2)
            # cap on the gap-facing end of the pipe
            cap_y = rect.bottom - settings.PIPE_CAP_HEIGHT if is_top else rect.y
            cap = pygame.Rect(
                rect.x - settings.PIPE_CAP_OVERHANG,
                cap_y,
                settings.PIPE_WIDTH + 2 * settings.PIPE_CAP_OVERHANG,
                settings.PIPE_CAP_HEIGHT,
            )
            pygame.draw.rect(surface, settings.GREEN, cap, border_radius=3)
            pygame.draw.rect(surface, settings.DARK_GREEN, cap, 2, border_radius=3)