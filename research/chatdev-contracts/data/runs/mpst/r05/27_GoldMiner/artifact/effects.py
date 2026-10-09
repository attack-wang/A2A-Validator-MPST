"""Visual effects: particle bursts and floating score texts."""
import math
import random
import pygame
from settings import *
class Particle:
    """One small moving dot with gravity and fading life."""
    def __init__(self, x, y, vx, vy, life, color, size):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.life = life
        self.max_life = life
        self.color = color
        self.size = size
    def update(self, dt):
        self.vy += PARTICLE_GRAVITY * dt
        self.x += self.vx * dt
        self.y += self.vy * dt
        self.life -= dt
        return self.life > 0
    def draw(self, surface):
        if self.life <= 0:
            return
        fade = max(0.0, min(1.0, self.life / self.max_life))
        color = tuple(int(c * fade) for c in self.color)
        r = max(1, int(self.size * fade))
        pygame.draw.circle(surface, color, (int(self.x), int(self.y)), r)
class ParticleSystem:
    """Container that spawns and animates particle bursts."""
    def __init__(self):
        self.particles = []
    def emit_burst(self, x, y, color, count=20, speed=200):
        for _ in range(count):
            ang = random.uniform(0, math.tau)
            spd = random.uniform(speed * 0.3, speed)
            life = random.uniform(0.4, 0.9)
            size = random.randint(2, 5)
            self.particles.append(Particle(
                x, y, math.cos(ang) * spd, math.sin(ang) * spd - speed * 0.3,
                life, color, size))
    def update(self, dt):
        self.particles = [p for p in self.particles if p.update(dt)]
    def draw(self, surface):
        for p in self.particles:
            p.draw(surface)
class FloatingText:
    """A short text that rises and fades out."""
    def __init__(self, x, y, text, color, life=1.2):
        self.x = x
        self.y = y
        self.text = text
        self.color = color
        self.life = life
        self.max_life = life
        self.font = pygame.font.SysFont("arial", 22, bold=True)
    def update(self, dt):
        self.y -= 40 * dt
        self.life -= dt
        return self.life > 0
    def draw(self, surface):
        if self.life <= 0:
            return
        fade = max(0.0, min(1.0, self.life / self.max_life))
        color = tuple(int(c * fade) for c in self.color)
        label = self.font.render(self.text, True, color)
        surface.blit(label, label.get_rect(center=(self.x, self.y)))
class TextSystem:
    """Container for floating texts."""
    def __init__(self):
        self.texts = []
    def add(self, x, y, text, color, life=1.2):
        self.texts.append(FloatingText(x, y, text, color, life))
    def update(self, dt):
        self.texts = [t for t in self.texts if t.update(dt)]
    def draw(self, surface):
        for t in self.texts:
            t.draw(surface)