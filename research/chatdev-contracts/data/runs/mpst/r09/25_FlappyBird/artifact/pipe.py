'''
Pipe pair entity: gap positioning, movement, and rendering.
'''
import pygame
import settings
class PipePair:
    def __init__(self, x, gap_center, gap_size, speed):
        self.x = float(x)
        self.width = settings.PIPE_WIDTH
        self.gap_center = float(gap_center)
        self.gap_size = float(gap_size)
        self.speed = float(speed)
        self.passed = False
        self._clamp_gap()
        self._sync_rects()
    def _clamp_gap(self):
        margin = self.gap_size / 2 + settings.PIPE_OVERHANG
        self.gap_center = max(margin, min(settings.GROUND_Y - margin, self.gap_center))
    def _sync_rects(self):
        gap_top = self.gap_center - self.gap_size / 2
        gap_bottom = self.gap_center + self.gap_size / 2
        self.top_rect = pygame.Rect(int(self.x), -settings.PIPE_OVERHANG, self.width, int(gap_top + settings.PIPE_OVERHANG))
        self.bottom_rect = pygame.Rect(int(self.x), int(gap_bottom), self.width, settings.GROUND_Y - int(gap_bottom))
    def update(self, dt, speed=None):
        if speed is not None:
            self.speed = float(speed)
        self.x -= self.speed * dt
        self._sync_rects()
    def off_screen(self):
        return self.x + self.width < -10
    def draw(self, surface):
        self._draw_pipe(surface, self.top_rect, cap_at_bottom=True)
        self._draw_pipe(surface, self.bottom_rect, cap_at_bottom=False)
    def _draw_pipe(self, surface, body, cap_at_bottom):
        if body.height <= 0:
            return
        pygame.draw.rect(surface, settings.PIPE_GREEN, body)
        light = pygame.Rect(body.left + 5, body.top, 10, body.height)
        pygame.draw.rect(surface, settings.PIPE_LIGHT, light)
        dark = pygame.Rect(body.right - 12, body.top, 7, body.height)
        pygame.draw.rect(surface, settings.PIPE_DARK, dark)
        pygame.draw.rect(surface, settings.PIPE_DARK, body, 2)
        cap_y = body.bottom - settings.CAP_H if cap_at_bottom else body.top
        cap = pygame.Rect(body.left - 4, cap_y, self.width + 8, settings.CAP_H)
        pygame.draw.rect(surface, settings.PIPE_GREEN, cap)
        pygame.draw.rect(surface, settings.PIPE_LIGHT, (cap.left + 5, cap.top, 10, cap.height))
        pygame.draw.rect(surface, settings.PIPE_DARK, (cap.right - 12, cap.top, 7, cap.height))
        pygame.draw.rect(surface, settings.PIPE_DARK, cap, 2)