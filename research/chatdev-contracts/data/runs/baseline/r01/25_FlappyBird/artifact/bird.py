"""Bird entity: physics, rendering, and collision surface."""
import math
import pygame
import settings
class Bird:
    """The player-controlled bird with gravity physics and flap impulse."""
    def __init__(self, x, y):
        self.start_x = x
        self.start_y = y
        self.x = float(x)
        self.y = float(y)
        self.velocity = 0.0
        self.rotation = 0.0
        self.radius = settings.BIRD_RADIUS
        self._flap_animation_timer = 0.0
        self._frames = [self._build_base_image(offset) for offset in (-4, 0, 4)]
        self._wing_phase = 0.0
    def _build_base_image(self, wing_offset=0):
        """Pre-render the bird (body, wing, eye, beak) onto a transparent surface."""
        diameter = self.radius * 2 + 8
        surface = pygame.Surface((diameter + 10, diameter), pygame.SRCALPHA)
        center_x = diameter // 2 + 2
        center_y = diameter // 2
        pygame.draw.circle(surface, settings.BIRD_BODY_COLOR, (center_x, center_y), self.radius)
        pygame.draw.circle(surface, settings.BIRD_WING_COLOR, (center_x, center_y), self.radius, 2)
        wing_rect = pygame.Rect(0, 0, self.radius + 6, self.radius - 4)
        wing_rect.center = (center_x - 3, center_y + 2 + wing_offset)
        pygame.draw.ellipse(surface, settings.BIRD_WING_COLOR, wing_rect)
        eye_pos = (center_x + self.radius // 2, center_y - self.radius // 2)
        pygame.draw.circle(surface, settings.BIRD_EYE_COLOR, eye_pos, 5)
        pygame.draw.circle(surface, settings.BIRD_PUPIL_COLOR, eye_pos, 2)
        beak_tip = (center_x + self.radius + 8, center_y + 2)
        beak_top = (center_x + self.radius - 4, center_y - 3)
        beak_bottom = (center_x + self.radius - 4, center_y + 7)
        pygame.draw.polygon(surface, settings.BIRD_BEAK_COLOR, [beak_top, beak_tip, beak_bottom])
        return surface
    def flap(self):
        """Apply an upward impulse and trigger the fast wing animation."""
        self.velocity = settings.FLAP_STRENGTH
        self._flap_animation_timer = 0.25
    def update(self, dt):
        """Apply gravity, integrate motion, and update tilt."""
        self.velocity = min(self.velocity + settings.GRAVITY * dt, settings.MAX_FALL_SPEED)
        self.y += self.velocity * dt
        if self.velocity < 0:
            target = settings.ROTATION_UP
        else:
            target = -settings.ROTATION_DOWN_MAX * min(1.0, self.velocity / settings.MAX_FALL_SPEED)
        self.rotation += (target - self.rotation) * min(1.0, dt * 12.0)
    def animate_wings(self, dt):
        """Advance the wing flap animation."""
        self._advance_wing_phase(dt, base_rate=10.0)
    def _advance_wing_phase(self, dt, base_rate):
        """Advance wing phase; flap timer speeds up the animation."""
        rate = base_rate * (3.0 if self._flap_animation_timer > 0 else 1.0)
        self._wing_phase += rate * dt
        self._flap_animation_timer = max(0.0, self._flap_animation_timer - dt)
    @property
    def _frame(self):
        """Return the current pre-rendered wing frame."""
        pattern = (0, 1, 2, 1)
        return self._frames[pattern[int(self._wing_phase) % 4]]
    def get_rect(self):
        """Return a collision rect slightly smaller than the sprite."""
        size = self.radius * 2 - 6
        return pygame.Rect(int(self.x - size / 2), int(self.y - size / 2), size, size)
    def draw(self, surface):
        """Draw the rotated bird sprite at its current position."""
        rotated = pygame.transform.rotate(self._frame, self.rotation)
        rect = rotated.get_rect(center=(int(self.x), int(self.y)))
        surface.blit(rotated, rect)
    def reset(self):
        """Restore the bird to its starting position and state."""
        self.x = float(self.start_x)
        self.y = float(self.start_y)
        self.velocity = 0.0
        self.rotation = 0.0
        self._flap_animation_timer = 0.0
        self._wing_phase = 0.0