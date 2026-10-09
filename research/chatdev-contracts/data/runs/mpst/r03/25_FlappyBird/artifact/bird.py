"""Bird entity: physics, animation, rendering."""
import math
import pygame
import settings as cfg
from utils import clamp
class Bird:
    def __init__(self, x, y):
        self.x = float(x)
        self.y = float(y)
        self.velocity = 0.0
        self.rotation = 0.0
        self.wing_timer = 0.0  # wing animation timer
        self._frames = self._build_frames()
    def _build_frames(self):
        """Pre-render 3 wing-position frames of the bird facing right."""
        frames = []
        r = cfg.BIRD_RADIUS
        size = int(r * 2.6)
        for wing_pos in (-1, 0, 1):
            s = pygame.Surface((size, size), pygame.SRCALPHA)
            cx = size * 0.45
            cy = size / 2
            # body
            pygame.draw.circle(s, cfg.BIRD_BODY, (int(cx), int(cy)), r)
            # belly highlight
            pygame.draw.circle(s, (255, 230, 120), (int(cx - r * 0.25), int(cy + r * 0.3)), int(r * 0.55))
            # wing
            wing = pygame.Surface((int(r * 1.2), int(r * 0.8)), pygame.SRCALPHA)
            pygame.draw.ellipse(wing, cfg.BIRD_WING, wing.get_rect())
            wing_rect = wing.get_rect(center=(int(cx - r * 0.2), int(cy + wing_pos * r * 0.45)))
            s.blit(wing, wing_rect)
            # eye
            pygame.draw.circle(s, cfg.BIRD_EYE, (int(cx + r * 0.45), int(cy - r * 0.35)), int(r * 0.38))
            pygame.draw.circle(s, cfg.BIRD_PUPIL, (int(cx + r * 0.55), int(cy - r * 0.35)), int(r * 0.16))
            # beak
            beak = [
                (cx + r * 0.8, cy - r * 0.15),
                (cx + r * 1.5, cy + r * 0.05),
                (cx + r * 0.8, cy + r * 0.35),
            ]
            pygame.draw.polygon(s, cfg.BIRD_BEAK, beak)
            frames.append(s)
        return frames
    def flap(self):
        """Apply an upward impulse."""
        self.velocity = cfg.FLAP_VELOCITY
        self.wing_timer = 0.0  # restart wing flap animation
    def update(self, dt):
        """Advance physics and animation timers."""
        self.velocity += cfg.GRAVITY * dt
        self.velocity = min(self.velocity, cfg.MAX_FALL_SPEED)
        self.y += self.velocity * dt
        # ceiling clamp
        if self.y - cfg.BIRD_RADIUS < 0:
            self.y = cfg.BIRD_RADIUS
            self.velocity = max(self.velocity, 0.0)
        self.wing_timer += dt
        # rotation eases toward velocity-based target
        target = clamp(-self.velocity * 0.12, -60.0, 25.0)
        rate = 12.0 if target > self.rotation else 6.0
        self.rotation += (target - self.rotation) * min(1.0, rate * dt)
    def draw(self, surface):
        """Draw the rotated, wing-animated bird."""
        frame = self._frames[[0, 1, 2, 1][int(self.wing_timer * 12) % 4]]
        rotated = pygame.transform.rotate(frame, self.rotation)
        rect = rotated.get_rect(center=(int(self.x), int(self.y)))
        surface.blit(rotated, rect)