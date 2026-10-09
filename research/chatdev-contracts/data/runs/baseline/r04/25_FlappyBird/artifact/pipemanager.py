'''
Pipe obstacles management: spawning, movement, difficulty scaling.
'''
import random
import pygame
import settings
from pipes import PipePair
class PipeManager:
    '''Spawns, moves, recycles pipes and scales difficulty with the score.'''
    def __init__(self):
        self.pipes = []
        self.distance_since_spawn = 0
    def reset(self):
        self.pipes.clear()
        self.distance_since_spawn = 0
    def current_speed(self, score):
        return min(settings.PIPE_SPEED_BASE + score * settings.PIPE_SPEED_INCREMENT,
                   settings.PIPE_SPEED_MAX)
    def current_gap(self, score):
        base = max(settings.BASE_GAP - score * settings.GAP_SHRINK_PER_POINT, settings.MIN_GAP)
        return base
    def update(self, score):
        '''Move pipes, spawn new ones, drop off-screen ones. Returns nothing.'''
        speed = self.current_speed(score)
        for pipe in self.pipes:
            pipe.update(speed)
        self.distance_since_spawn += speed
        if self.distance_since_spawn >= settings.PIPE_SPACING or not self.pipes:
            self.spawn(score)
            self.distance_since_spawn = 0
        self.pipes = [p for p in self.pipes if not p.off_screen]
    def spawn(self, score):
        gap = self.current_gap(score)
        # random variation
        gap = max(settings.MIN_GAP, gap + random.randint(-settings.GAP_VARIATION, settings.GAP_VARIATION))
        margin = 60
        min_center = margin + gap / 2
        max_center = settings.SCREEN_HEIGHT - settings.GROUND_HEIGHT - margin - gap / 2
        gap_center = random.uniform(min_center, max_center)
        x = settings.SCREEN_WIDTH + 10
        self.pipes.append(PipePair(x, gap_center, gap))