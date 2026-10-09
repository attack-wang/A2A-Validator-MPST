"""Pipe obstacles and the manager that spawns/moves/scores them."""
import random
import pygame
import settings as cfg
from utils import circle_rect_collision
class Pipe:
    """A single pipe pair (top + bottom) with a vertical gap."""
    def __init__(self, x, gap_center, gap_height):
        self.x = float(x)
        self.gap_center = float(gap_center)
        self.gap_height = float(gap_height)
        self.scored = False
        self._sync_rects()
    def _sync_rects(self):
        """Recompute collision rects from the current x and gap geometry."""
        w = cfg.PIPE_WIDTH
        ground_y = cfg.HEIGHT - cfg.GROUND_HEIGHT
        gap_top = self.gap_center - self.gap_height / 2
        gap_bottom = self.gap_center + self.gap_height / 2
        self.top_rect = pygame.Rect(round(self.x), 0, w, round(gap_top))
        self.bottom_rect = pygame.Rect(round(self.x), round(gap_bottom), w, round(ground_y - gap_bottom))
    def update(self, dt, speed):
        """Move left at the manager-level speed (shared by all pipes)."""
        self.x -= speed * dt
        self._sync_rects()
    def offscreen(self):
        """True once the pipe (including its lip) has fully left the screen."""
        return self.x + cfg.PIPE_WIDTH < -40
    def draw(self, surface):
        """Render body, shading stripes, outline, and gap lips."""
        w = cfg.PIPE_WIDTH
        lip_h = 26
        for rect in (self.top_rect, self.bottom_rect):
            pygame.draw.rect(surface, cfg.PIPE_GREEN, rect)
            pygame.draw.rect(surface, cfg.PIPE_LIGHT, (rect.left + 4, rect.top, 10, rect.height))
            pygame.draw.rect(surface, cfg.PIPE_DARK, (rect.right - 12, rect.top, 8, rect.height))
            pygame.draw.rect(surface, cfg.PIPE_DARK, rect, 2)
        # lips
        top_lip = pygame.Rect(self.top_rect.left - 4, self.top_rect.bottom - lip_h, w + 8, lip_h)
        bottom_lip = pygame.Rect(self.bottom_rect.left - 4, self.bottom_rect.top, w + 8, lip_h)
        for lip in (top_lip, bottom_lip):
            pygame.draw.rect(surface, cfg.PIPE_GREEN, lip)
            pygame.draw.rect(surface, cfg.PIPE_LIGHT, (lip.left + 4, lip.top, 10, lip.height))
            pygame.draw.rect(surface, cfg.PIPE_DARK, lip, 2)
class PipeManager:
    """Spawns pipes at fixed horizontal intervals with score-scaled difficulty."""
    def __init__(self):
        self.pipes = []
        self.distance_since_spawn = 0.0
        self.speed = cfg.BASE_SPEED
        self.gap_height = cfg.BASE_GAP
    def reset(self):
        """Clear pipes and restore starting difficulty."""
        self.pipes.clear()
        self.distance_since_spawn = 0.0
        self.speed = cfg.BASE_SPEED
        self.gap_height = cfg.BASE_GAP
    def difficulty(self, score):
        """Compute current (gap_height, speed) from the score."""
        gap = max(cfg.MIN_GAP, cfg.BASE_GAP - score * cfg.GAP_SHRINK_PER_POINT)
        speed = min(cfg.MAX_SPEED, cfg.BASE_SPEED + score * cfg.SPEED_INCREMENT_PER_POINT)
        return gap, speed
    def spawn(self, x, gap_height):
        """Create a pipe at x with a randomly placed vertical gap."""
        ground_y = cfg.HEIGHT - cfg.GROUND_HEIGHT
        lo = cfg.GAP_MARGIN + gap_height / 2
        hi = ground_y - cfg.GAP_MARGIN - gap_height / 2
        center = random.uniform(lo, hi)
        self.pipes.append(Pipe(x, center, gap_height))
    def update(self, dt, score):
        """Advance all pipes at one shared speed and spawn on distance."""
        self.gap_height, self.speed = self.difficulty(score)
        self.distance_since_spawn += self.speed * dt
        if self.distance_since_spawn >= cfg.PIPE_SPACING:
            self.distance_since_spawn -= cfg.PIPE_SPACING
            self.spawn(cfg.WIDTH + 40, self.gap_height)
        for p in self.pipes:
            p.update(dt, self.speed)
        self.pipes = [p for p in self.pipes if not p.offscreen()]
    def update_score(self, bird_x):
        """Award one point per pipe whose right edge has passed the bird."""
        points = 0
        for p in self.pipes:
            if not p.scored and p.x + cfg.PIPE_WIDTH < bird_x:
                p.scored = True
                points += 1
        return points
    def draw(self, surface):
        """Draw every pipe."""
        for p in self.pipes:
            p.draw(surface)