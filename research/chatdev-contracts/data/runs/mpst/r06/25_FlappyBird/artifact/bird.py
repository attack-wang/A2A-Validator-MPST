'''
bird.py
Bird entity: physics (gravity / flap impulse), rotation animation,
collision rectangle and self-contained rendering (no external assets).
'''
import math
import pygame
from settings import (
    BIRD_RADIUS, GRAVITY, FLAP_VELOCITY, MAX_FALL_SPEED,
    MAX_ROTATION_UP, MAX_ROTATION_DOWN,
    BIRD_YELLOW, BIRD_ORANGE, BIRD_WHITE, BIRD_BLACK,
)
class Bird:
    """The player-controlled bird."""
    def __init__(self, x, y):
        self.x = float(x)
        self.y = float(y)
        self.velocity = 0.0
        self.rotation = 0.0
        self.wing_phase = 0        # drives the wing flap animation
        self.flap_burst = 0        # frames of fast wing movement after a flap
    # ------------------------------------------------------------------ #
    # Behaviour
    # ------------------------------------------------------------------ #
    def flap(self):
        """Apply an upward impulse and start the fast wing animation."""
        self.velocity = FLAP_VELOCITY
        self.rotation = MAX_ROTATION_UP
        self.flap_burst = 8
    def update(self):
        """Advance physics and animation one frame."""
        # Gravity
        self.velocity = min(self.velocity + GRAVITY, MAX_FALL_SPEED)
        self.y += self.velocity
        # Rotation: nose up right after a flap, nose dive while falling
        if self.velocity < 0:
            self.rotation = max(MAX_ROTATION_UP, self.rotation - 6)
        else:
            self.rotation = min(MAX_ROTATION_DOWN, self.rotation + 2.5)
        # Wing animation
        self.flap_burst = max(0, self.flap_burst - 1)
        self.wing_phase += 3 if self.flap_burst else 1
    @property
    def rect(self):
        """Collision rectangle, slightly inset for fairer hit detection."""
        inset = 3
        return pygame.Rect(
            int(self.x - BIRD_RADIUS + inset),
            int(self.y - BIRD_RADIUS + inset),
            (BIRD_RADIUS - inset) * 2,
            (BIRD_RADIUS - inset) * 2,
        )
    # ------------------------------------------------------------------ #
    # Rendering
    # ------------------------------------------------------------------ #
    def _draw_body(self):
        """Draw the (un-rotated) bird onto a small transparent surface."""
        r = BIRD_RADIUS
        size = r * 2 + 8
        img = pygame.Surface((size, size), pygame.SRCALPHA)
        cx, cy = size // 2, size // 2
        # Body
        pygame.draw.circle(img, BIRD_YELLOW, (cx, cy), r)
        pygame.draw.circle(img, BIRD_ORANGE, (cx, cy), r, 2)
        # Belly
        pygame.draw.ellipse(img, BIRD_WHITE, (cx - r + 4, cy, r * 2 - 10, r - 4))
        # Wing (animated)
        offset = int(math.sin(math.radians(self.wing_phase % 360)) * 4)
        wing_y = cy + 2 + offset
        pygame.draw.ellipse(img, BIRD_ORANGE, (cx - r + 2, wing_y, r + 2, 7))
        # Eye
        pygame.draw.circle(img, BIRD_WHITE, (cx + 6, cy - 5), 5)
        pygame.draw.circle(img, BIRD_BLACK, (cx + 8, cy - 5), 2)
        # Beak
        pygame.draw.polygon(img, BIRD_ORANGE, [
            (cx + r - 2, cy - 1), (cx + r + 7, cy + 1), (cx + r - 2, cy + 5),
        ])
        return img
    def draw(self, surface):
        """Draw the bird rotated to match its current tilt."""
        img = self._draw_body()
        img = pygame.transform.rotate(img, -self.rotation)
        rect = img.get_rect(center=(int(self.x), int(self.y)))
        surface.blit(img, rect)