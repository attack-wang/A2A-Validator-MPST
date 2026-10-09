'''
pipe_manager.py
Owns the collection of active pipes: spawning at random gap positions,
scrolling, off-screen cleanup, scoring and collision checks.
The spawn gap size follows the current score via settings.gap_size_for_score,
so difficulty ramps up as the player progresses.
'''
import random
import pygame
import settings
from pipe import Pipe
class PipeManager:
    """Spawns, moves, scores and draws every pipe on screen."""
    def __init__(self):
        self.pipes = []
        self.spawn_timer = 0.0
        self.score = 0  # kept in sync by the Game each frame
    # ------------------------------------------------------------- setup
    def reset(self):
        """Clear all pipes and timers for a fresh round."""
        self.pipes = []
        self.spawn_timer = 0.0
        self.score = 0
    # ------------------------------------------------------------- update
    def update(self, dt, speed, interval):
        """Scroll pipes, drop off-screen ones and spawn on the interval."""
        for pipe in self.pipes:
            pipe.update(dt, speed)
        self.pipes = [p for p in self.pipes if not p.is_offscreen()]
        self.spawn_timer += dt
        if self.spawn_timer >= interval:
            self.spawn_timer = 0.0
            self._spawn()
    def _spawn(self):
        """Create a new pipe just off the right edge with a random gap."""
        gap = settings.gap_size_for_score(self.score)
        min_center = settings.GAP_MARGIN + gap / 2.0
        max_center = settings.SKY_HEIGHT - settings.GAP_MARGIN - gap / 2.0
        gap_center = random.uniform(min_center, max_center)
        self.pipes.append(Pipe(settings.SCREEN_WIDTH + 10, gap_center, gap))
    # ---------------------------------------------------------- scoring
    def update_score(self, bird_x):
        """Mark passed pipes; returns how many new pipes were passed."""
        gained = 0
        for pipe in self.pipes:
            if not pipe.scored and pipe.x + settings.PIPE_WIDTH < bird_x:
                pipe.scored = True
                gained += 1
        return gained
    # -------------------------------------------------------- collision
    def collides(self, bird_rect):
        """True when the bird's rect intersects any pipe section."""
        for pipe in self.pipes:
            top_rect, bottom_rect = pipe.get_rects()
            if bird_rect.colliderect(top_rect) or bird_rect.colliderect(bottom_rect):
                return True
        return False
    # -------------------------------------------------------------- draw
    def draw(self, surface):
        """Draw every active pipe."""
        for pipe in self.pipes:
            pipe.draw(surface)