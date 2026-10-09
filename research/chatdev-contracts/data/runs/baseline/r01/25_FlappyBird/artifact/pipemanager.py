"""Pipe spawning, movement, and difficulty-driven gap/speed management."""
import random
import pygame
import settings
from pipe import Pipe
class PipeManager:
    """Owns all active pipes: spawning, scrolling, collision, and cleanup."""
    def __init__(self):
        self.pipes = []
        self.gap_size = settings.BASE_GAP_SIZE
        self.speed = settings.BASE_PIPE_SPEED
    def set_difficulty(self, gap_size, speed):
        """Apply new difficulty values to future spawns and existing pipes."""
        self.gap_size = gap_size
        self.speed = speed
        for pipe in self.pipes:
            pipe.speed = speed
    def update(self, dt):
        """Scroll pipes, spawn new ones at fixed intervals, drop offscreen ones."""
        for pipe in self.pipes:
            pipe.update(dt)
        spawn_x = settings.SCREEN_WIDTH + settings.PIPE_CAP_OVERHANG
        if not self.pipes:
            self.pipes.append(self._spawn_pipe(spawn_x))
        else:
            last = max(self.pipes, key=lambda p: p.x)
            if last.x <= settings.SCREEN_WIDTH - settings.PIPE_SPAWN_DISTANCE:
                self.pipes.append(self._spawn_pipe(spawn_x))
        self.pipes = [p for p in self.pipes if not p.is_offscreen()]
    def _spawn_pipe(self, x):
        """Create a pipe with a randomized gap center and size variance."""
        playable = settings.SCREEN_HEIGHT - settings.GROUND_HEIGHT
        margin = 40
        gap = max(settings.MIN_GAP_SIZE,
                  self.gap_size + random.uniform(-settings.GAP_VARIANCE, settings.GAP_VARIANCE))
        half = gap / 2  # bounds use the actual (varied) gap size
        min_center = half + margin
        max_center = playable - half - margin
        center = random.uniform(min_center, max_center)
        return Pipe(x, center, gap, self.speed)
    def collides_with(self, rect):
        """Return True if the given rect hits any active pipe."""
        return any(pipe.collides_with(rect) for pipe in self.pipes)
    def draw(self, surface):
        """Draw every active pipe."""
        for pipe in self.pipes:
            pipe.draw(surface)