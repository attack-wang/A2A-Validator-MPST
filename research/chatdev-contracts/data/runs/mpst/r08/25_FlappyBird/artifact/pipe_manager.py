'''
Spawns and manages pipes, implementing the difficulty curve.
'''
import random
import pygame
import settings
from pipe import Pipe
class PipeManager:
    """Owns the active pipe list, spawn timing and difficulty scaling."""
    def __init__(self):
        self.pipes = []
        self.distance_since_spawn = 0.0
        self.started = False
        self.start_timer = 0.0
    def reset(self):
        """Clear all pipes and restart the spawn timer."""
        self.pipes.clear()
        self.distance_since_spawn = 0.0
        self.started = False
        self.start_timer = 0.0
    def current_speed(self, score):
        """World speed ramps up with the score."""
        return min(settings.MAX_PIPE_SPEED,
                   settings.BASE_PIPE_SPEED + score * settings.SPEED_GAIN_PER_POINT)
    def current_gap(self, score):
        """Gap size shrinks with the score, with some randomness."""
        target = max(settings.MIN_GAP_SIZE,
                     settings.BASE_GAP_SIZE - score * settings.GAP_SHRINK_PER_POINT)
        spread = (target - settings.MIN_GAP_SIZE) * settings.GAP_RANDOMNESS
        gap = random.uniform(target - spread, target + spread)
        return max(settings.MIN_GAP_SIZE, min(settings.BASE_GAP_SIZE, gap))
    def _spawn(self, score):
        """Create a new pipe just off the right edge of the screen."""
        gap = self.current_gap(score)
        margin = 60
        ground_top = settings.SCREEN_HEIGHT - settings.GROUND_HEIGHT
        lo = gap / 2 + margin
        hi = ground_top - gap / 2 - margin
        center = random.uniform(lo, hi)
        self.pipes.append(Pipe(settings.SCREEN_WIDTH + settings.PIPE_WIDTH,
                               center, gap, self.current_speed(score)))
    def update(self, dt, score):
        """Move pipes, spawn new ones, drop off-screen ones."""
        speed = self.current_speed(score)
        if not self.started:
            self.start_timer += dt
            if self.start_timer >= settings.FIRST_PIPE_DELAY:
                self.started = True
                self._spawn(score)
                self.distance_since_spawn = 0.0
        else:
            self.distance_since_spawn += speed * dt
            if self.distance_since_spawn >= settings.PIPE_SPACING:
                self.distance_since_spawn -= settings.PIPE_SPACING
                self._spawn(score)
        for pipe in self.pipes:
            pipe.update(dt, speed)
        self.pipes = [p for p in self.pipes if not p.is_offscreen()]
    def collides(self, rect):
        """True if any active pipe overlaps the given rect."""
        return any(p.collides(rect) for p in self.pipes)
    def pipes_passed(self, bird_x):
        """Returns number of pipes newly passed (for scoring)."""
        return sum(1 for p in self.pipes if p.has_passed(bird_x))
    def draw(self, screen):
        """Render all active pipes."""
        for p in self.pipes:
            p.draw(screen)