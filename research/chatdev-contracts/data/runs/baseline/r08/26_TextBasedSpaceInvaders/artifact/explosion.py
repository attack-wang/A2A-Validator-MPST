'''
explosion.py
A short-lived particle burst displayed when something is destroyed.
Pure-python particle simulation; rendered as small fading squares.
'''
import math
import random
from settings import Settings
class Explosion:
    """A short-lived particle burst displayed when something is destroyed."""
    def __init__(self, center, color, particle_count=16, max_life=0.55):
        self.done = False
        self.particles = []
        for _ in range(particle_count):
            angle = random.uniform(0.0, math.tau)
            speed = random.uniform(40.0, 190.0)
            life = random.uniform(max_life * 0.5, max_life)
            self.particles.append({
                "pos": [float(center[0]), float(center[1])],
                "vel": [math.cos(angle) * speed, math.sin(angle) * speed],
                "life": life,
                "max_life": life,
                "color": color,
                "size": random.randint(2, 4),
            })
    def update(self, dt):
        alive = False
        for p in self.particles:
            if p["life"] <= 0:
                continue
            alive = True
            p["life"] -= dt
            p["pos"][0] += p["vel"][0] * dt
            p["pos"][1] += p["vel"][1] * dt
            p["vel"][1] += 120.0 * dt
        if not alive:
            self.done = True
    def draw(self, canvas):
        for p in self.particles:
            if p["life"] <= 0:
                continue
            fade = max(0.0, p["life"] / p["max_life"])
            size = max(1, int(p["size"] * fade + 1))
            half = size / 2.0
            canvas.create_rectangle(
                p["pos"][0] - half, p["pos"][1] - half,
                p["pos"][0] + half, p["pos"][1] + half,
                fill=p["color"], outline="")