'''
effects.py
Transient visual effects: explosions (TNT) and floating score texts.
'''
import pygame
import settings
class Explosion:
    def __init__(self, x, y):
        self.x = x; self.y = y
        self.timer = 0.0
        self.duration = 0.6
        self.max_radius = 90
    @property
    def finished(self):
        return self.timer >= self.duration
    def update(self, dt):
        self.timer += dt
    def draw(self, surface):
        progress = self.timer / self.duration
        radius = int(self.max_radius * progress)
        alpha... # pygame circles don't support alpha directly on surface; draw ring
        # draw expanding ring + inner flash