'''
Bird module: defines the Bird entity controlled by the player.
'''
import math
import pygame
from settings import *
class Bird:
    """The player-controlled bird. Handles physics, animation and drawing."""
    def __init__(self, x, y):
        self.start_x = x
        self.start_y = y
        self.reset()
    def reset(self):
        self.x = self.start_x
        self.y = self.start_y
        self.vel = 0.0
        self.rotation = 0.0
        self.radius = BIRD_RADIUS
        self.wing_timer = 0
    def flap(self):
        self.vel = FLAP_STRENGTH
        self.wing_timer = WING_FLAP_FRAMES
    def update(self):
        self.vel = min(self.vel + GRAVITY, MAX_FALL_SPEED)
        self.y += self.vel
        if self.y < self.radius:
            self.y = self.radius
            self.vel = 0
        # smooth rotation toward target
        target = max(-25, min(80, self.vel * 5))
        self.rotation += (target - self.rotation) * 0.2
        if self.wing_timer > 0:
            self.wing_timer -= 1
    @property
    def rect(self):
        r = self.radius - 3  # forgiving hitbox
        return pygame.Rect(self.x - r, self.y - r, r * 2, r * 2)
    def draw(self, surface):
        ...