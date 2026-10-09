"""Bird entity: physics, flapping, animation and collision helpers."""
import math
import pygame
import settings
import utils
class Bird:
    def __init__(self, x, y):
        self.x = float(x)
        self.y = float(y)
        self.velocity = 0.0
        self.rotation = 0.0
        self.wing_phase = 0.0
        self.radius = settings.BIRD_RADIUS
    def flap(self):
        self.velocity = settings.FLAP_VELOCITY
    def update(self, dt):
        # gravity
        self.velocity = min(self.velocity + settings.GRAVITY * dt, settings.MAX_FALL_SPEED)
        self.y += self.velocity * dt
        # keep the bird under the ceiling
        if self.y < self.radius:
            self.y = self.radius
            self.velocity = max(self.velocity, 0.0)
        # wing animation speeds up while flapping
        self.wing_phase += (10 if self.velocity < 0 else 5) * dt
        # tilt: nose up when rising, nose down when diving
        target = -25 if self.velocity < 0 else min(90, self.velocity / settings.MAX_FALL_SPEED * 90)
        self.rotation += (target - self.rotation) * min(1.0, dt * 10)
    def get_rect(self):
        return pygame.Rect(int(self.x - self.radius), int(self.y - self.radius),
                           self.radius * 2, self.radius * 2)
    def draw(self, surface):
        utils.draw_bird(surface, self.x, self.y, self.rotation, self.wing_phase)