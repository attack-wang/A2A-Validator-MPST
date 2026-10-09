"""
bird.py
The Bird entity: physics integration (gravity / flap impulse), tilt
rotation, wing animation and self-rendering.  The bird is drawn
procedurally (no external image assets required).
"""
import math
import pygame
from settings import (GRAVITY, FLAP_STRENGTH, MAX_FALL_SPEED, BIRD_RADIUS,
                      HITBOX_SHRINK, BIRD_BODY, BIRD_WING, BIRD_BELLY,
                      BEAK, EYE_WHITE, EYE_BLACK)
# rotation limits / smoothing
MAX_UP_ROT = -28.0      # degrees, nose up right after a flap
MAX_DOWN_ROT = 90.0     # degrees, nose dive while falling
ROT_SPEED = 9.0         # how fast rotation eases toward its target
WING_BASE_HZ = 7.0      # idle wing-beat frequency
WING_FAST_HZ = 16.0     # wing-beat frequency shortly after a flap
WING_FAST_TIME = 0.30   # seconds of fast beating after a flap
class Bird:
    """Player-controlled bird with gravity physics and procedural art."""
    def __init__(self, x, y):
        self.x = float(x)
        self.base_y = float(y)   # hover centre used on the start screen
        self.reset()
    def reset(self):
        self.y = self.base_y
        self.vel = 0.0
        self.rot = 0.0
        self.wing_phase = 0.0
        self.fast_wing = 0.0
        self.alive = True
    @property
    def radius(self):
        return BIRD_RADIUS
    def flap(self):
        """Apply an upward impulse and kick the wing animation."""
        self.vel = FLAP_STRENGTH
        self.fast_wing = WING_FAST_TIME
    def update(self, dt, physics=True):
        """Advance physics + animation.  `physics=False` = start-screen hover."""
        if physics:
            self.vel = min(self.vel + GRAVITY * dt, MAX_FALL_SPEED)
            self.y += self.vel * dt
        else:
            # gentle sinusoidal hover on the start screen
            self.y = self.base_y + math.sin(pygame.time.get_ticks() * 0.004) * 9.0
            self.rot = 0.0
        # wing animation
        self.fast_wing = max(0.0, self.fast_wing - dt)
        hz = WING_FAST_HZ if self.fast_wing > 0 else WING_BASE_HZ
        self.wing_phase += hz * dt * math.tau  # radians
        # rotation eases toward a velocity-dependent target
        if self.vel < 0:
            target = MAX_UP_ROT
        else:
            t = min(1.0, self.vel / MAX_FALL_SPEED)
            target = MAX_UP_ROT + (MAX_DOWN_ROT - MAX_UP_ROT) * t
        self.rot += (target - self.rot) * min(1.0, ROT_SPEED * dt)
    def get_rect(self):
        """Forgiving axis-aligned hit-box around the bird body."""
        r = BIRD_RADIUS * HITBOX_SHRINK
        return pygame.Rect(int(self.x - r), int(self.y - r),
                           int(r * 2), int(r * 2))
    def draw(self, surface):
        """Render the bird (rotated sprite built from primitives)."""
        size = int(BIRD_RADIUS * 3.2)
        sprite = pygame.Surface((size, size), pygame.SRCALPHA)
        c = size / 2
        r = BIRD_RADIUS
        # body
        pygame.draw.circle(sprite, BIRD_BODY, (int(c), int(c)), int(r))
        # belly
        pygame.draw.circle(sprite, BIRD_BELLY,
                           (int(c - r * 0.15), int(c + r * 0.45)), int(r * 0.55))
        # wing (animated, flaps around the body centre)
        wing_y = c + math.sin(self.wing_phase) * r * 0.35
        pygame.draw.ellipse(sprite, BIRD_WING,
                            (int(c - r * 0.95), int(wing_y - r * 0.30),
                             int(r * 1.15), int(r * 0.60)))
        # eye
        pygame.draw.circle(sprite, EYE_WHITE,
                           (int(c + r * 0.45), int(c - r * 0.35)), int(r * 0.32))
        pygame.draw.circle(sprite, EYE_BLACK,
                           (int(c + r * 0.55), int(c - r * 0.35)), int(r * 0.15))
        # beak
        pygame.draw.polygon(sprite, BEAK, [
            (c + r * 0.75, c - r * 0.10),
            (c + r * 1.55, c + r * 0.05),
            (c + r * 0.75, c + r * 0.30),
        ])
        # rotate around the centre and blit
        rotated = pygame.transform.rotate(sprite, -self.rot)
        rect = rotated.get_rect(center=(int(self.x), int(self.y)))
        surface.blit(rotated, rect)