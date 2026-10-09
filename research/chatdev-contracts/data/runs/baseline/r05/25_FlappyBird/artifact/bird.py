"""Bird entity: physics, flapping, and rendering."""
import math
import pygame
import settings
class Bird:
    """The player-controlled bird with gravity-based physics."""
    def __init__(self, x, y):
        self.x = float(x)
        self.y = float(y)
        self.velocity = 0.0
        self.rotation = 0.0
        self.wing_timer = 0.0
        self.alive = True
    def flap(self):
        """Apply an upward impulse and reset rotation upward."""
        self.velocity = settings.FLAP_STRENGTH
        self.rotation = -25.0
    def update(self, dt):
        """Advance physics: gravity, position, rotation, wing animation."""
        self.velocity = min(self.velocity + settings.GRAVITY * dt, settings.MAX_FALL_SPEED)
        self.y += self.velocity * dt
        # Rotate downward as the bird falls; snap up on flap.
        if self.velocity < 0:
            target = -25.0
        else:
            target = min(90.0, (self.velocity / settings.MAX_FALL_SPEED) * 90.0)
        self.rotation += (target - self.rotation) * min(1.0, dt * 12.0)
        # Wing flapping animation speeds up while rising.
        rate = 18.0 if self.velocity < 0 else 8.0
        self.wing_timer += dt * rate
    @property
    def rect(self):
        """Collision rectangle (slightly smaller than the sprite for fairness)."""
        r = settings.BIRD_RADIUS
        return pygame.Rect(int(self.x - r * 0.8), int(self.y - r * 0.8), int(r * 1.6), int(r * 1.6))
    def draw(self, surface):
        """Render the bird as a stylized shape rotated with its velocity."""
        r = settings.BIRD_RADIUS
        bird_surface = pygame.Surface((r * 4, r * 4), pygame.SRCALPHA)
        cx = cy = r * 2
        # Body
        pygame.draw.circle(bird_surface, settings.BIRD_BODY, (int(cx), int(cy)), r)
        # Belly highlight
        pygame.draw.circle(bird_surface, (255, 230, 120), (int(cx - r * 0.2), int(cy + r * 0.35)), int(r * 0.6))
        # Eye
        pygame.draw.circle(bird_surface, (255, 255, 255), (int(cx + r * 0.45), int(cy - r * 0.35)), int(r * 0.4))
        pygame.draw.circle(bird_surface, settings.BIRD_EYE, (int(cx + r * 0.55), int(cy - r * 0.35)), int(r * 0.18))
        # Beak
        beak_points = [
            (cx + r * 0.7, cy - r * 0.1),
            (cx + r * 1.5, cy + r * 0.1),
            (cx + r * 0.7, cy + r * 0.4),
        ]
        pygame.draw.polygon(bird_surface, settings.BIRD_BEAK, beak_points)
        # Wing (animated flapping)
        wing_phase = math.sin(self.wing_timer)
        wing_y = cy + wing_phase * r * 0.5
        wing_points = [
            (cx - r * 0.6, cy),
            (cx - r * 1.4, wing_y + r * 0.3),
            (cx - r * 0.2, wing_y + r * 0.5),
        ]
        pygame.draw.polygon(bird_surface, settings.BIRD_WING, wing_points)
        rotated = pygame.transform.rotate(bird_surface, -self.rotation)
        blit_pos = rotated.get_rect(center=(int(self.x), int(self.y))).topleft
        surface.blit(rotated, blit_pos)