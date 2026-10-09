'''
Bird entity: physics, input response and rendering.
'''
import math
import pygame
import settings
class Bird:
    """The player-controlled bird.
    Handles gravity-based physics, the flap impulse, visual rotation
    and collision rectangle generation.
    """
    def __init__(self, x, y):
        self.x = float(x)
        self.y = float(y)
        self.velocity = 0.0
        self.rotation = 0.0
        self.flap_animation = 0.0
        self.wing_phase = 0.0
        self.hover_time = 0.0
        self.alive = True
    def flap(self):
        """Apply an upward impulse and start the wing animation."""
        self.velocity = settings.FLAP_VELOCITY
        self.flap_animation = 0.25
    def idle_hover(self, dt):
        """Gentle bobbing used on the ready screen."""
        self.hover_time += dt
        base_y = settings.SCREEN_HEIGHT * 0.45
        self.y = base_y + math.sin(self.hover_time * 3.0) * 8.0
        self.rotation = math.sin(self.hover_time * 3.0) * 4.0
        self.wing_phase += dt * 10.0
    def update(self, dt):
        """Advance physics one frame; dt in seconds."""
        self.velocity = min(self.velocity + settings.GRAVITY * dt, settings.MAX_FALL_SPEED)
        self.y += self.velocity * dt
        # Tilt: nose up when rising, nose dive when falling.
        if self.velocity < 0:
            target = max(-25.0, self.velocity * 0.08)
        else:
            target = min(90.0, self.velocity * 0.13)
        self.rotation += (target - self.rotation) * min(1.0, dt * 12.0)
        # Wing animation timer.
        self.flap_animation = max(0.0, self.flap_animation - dt)
        self.wing_phase += dt * (28.0 if self.flap_animation > 0 else 10.0)
    def get_rect(self):
        """Collision rectangle (slightly forgiving square hitbox)."""
        size = int(settings.BIRD_RADIUS * 1.7)
        return pygame.Rect(int(self.x - size / 2), int(self.y - size / 2), size, size)
    def draw(self, screen):
        """Render the bird with rotation and animated wing."""
        size = int(settings.BIRD_RADIUS * 3)
        surf = pygame.Surface((size, size), pygame.SRCALPHA)
        cx = cy = size // 2
        r = settings.BIRD_RADIUS
        # body
        pygame.draw.ellipse(surf, settings.BIRD_BODY, (cx - r, cy - int(r * 0.8), r * 2, int(r * 1.6)))
        # belly
        pygame.draw.ellipse(surf, settings.BIRD_BELLY, (cx - r + 4, cy, int(r * 1.5), int(r * 1.1)))
        # wing
        wing_offset = math.sin(self.wing_phase) * r * 0.35
        pygame.draw.ellipse(surf, settings.BIRD_WING, (cx - int(r * 0.9), cy - int(r * 0.2) + int(wing_offset), int(r * 1.1), int(r * 0.7)))
        # eye
        pygame.draw.circle(surf, (255, 255, 255), (cx + int(r * 0.45), cy - int(r * 0.35)), int(r * 0.38))
        pygame.draw.circle(surf, settings.BIRD_EYE, (cx + int(r * 0.55), cy - int(r * 0.35)), int(r * 0.18))
        # beak
        beak = [(cx + int(r * 0.7), cy - 2), (cx + int(r * 1.5), cy + int(r * 0.15)), (cx + int(r * 0.7), cy + int(r * 0.45))]
        pygame.draw.polygon(surf, settings.BIRD_BEAK, beak)
        rotated = pygame.transform.rotate(surf, -self.rotation)
        rect = rotated.get_rect(center=(int(self.x), int(self.y)))
        screen.blit(rotated, rect)