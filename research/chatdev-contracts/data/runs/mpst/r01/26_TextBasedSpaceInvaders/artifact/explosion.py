'''
explosion.py: particle burst effect for destroyed aliens, bombs and the ship.
'''
import math
import random
import pygame
class Explosion:
    """A short-lived particle burst shown when an alien or bomb is destroyed."""
    def __init__(self, center, color, duration=0.4, particles=12):
        self.center = center
        self.color = color
        self.duration = duration
        self.life = duration
        self.particles = []
        for _ in range(particles):
            angle = random.uniform(0, math.tau)
            speed = random.uniform(40, 160)
            self.particles.append([math.cos(angle) * speed, math.sin(angle) * speed])
        self.positions = [list(center) for _ in range(particles)]
    def update(self, dt):
        self.life -= dt
        for pos, vel in zip(self.positions, self.particles):
            pos[0] += vel[0] * dt
            pos[1] += vel[1] * dt
    @property
    def expired(self):
        return self.life <= 0
    def draw(self, screen):
        t = max(0.0, self.life / self.duration)
        radius = max(1, int(3 * t + 1))
        for pos in self.positions:
            pygame.draw.circle(screen, self.color, (int(pos[0]), int(pos[1])), radius)