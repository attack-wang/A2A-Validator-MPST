"""Bird entity: physics, rotation, wing animation and rendering."""
import math
import pygame
import settings
class Bird:
    """The player-controlled bird with gravity, flapping and rotation."""
    def __init__(self, x, y):
        self.start_y = y
        self.x = float(x)
        self.y = float(y)
        self.velocity = 0.0
        self.gravity = settings.GRAVITY
        self.flap_strength = settings.FLAP_STRENGTH
        self.radius = settings.BIRD_RADIUS
        self.rotation = 0.0
    def flap(self):
        """Give the bird an upward impulse."""
        self.velocity = self.flap_strength
    def reset(self, x, y):
        """Restore the bird to its initial state for a new round."""
        self.x = float(x)
        self.y = float(y)
        self.velocity = 0.0
        self.rotation = 0.0
    def update(self):
        """Apply gravity, integrate position and ease rotation toward velocity."""
        self.velocity = min(self.velocity + self.gravity, settings.MAX_FALL_SPEED)
        self.y += self.velocity
        target = max(-25.0, min(90.0, self.velocity * 7.0))
        self.rotation += (target - self.rotation) * 0.2
    def get_rect(self):
        """Axis-aligned bounding box used for pipe collisions."""
        return pygame.Rect(int(self.x - self.radius), int(self.y - self.radius),
                           self.radius * 2, self.radius * 2)
    def draw(self, screen):
        """Draw the bird (body, wing, eye, beak) rotated by self.rotation."""
        size = self.radius * 2 + 16
        surf = pygame.Surface((size, size), pygame.SRCALPHA)
        cx = size // 2
        cy = size // 2
        # body
        pygame.draw.circle(surf, settings.YELLOW, (cx, cy), self.radius)
        pygame.draw.circle(surf, settings.ORANGE, (cx, cy), self.radius, 2)
        # flapping wing
        wing_phase = math.sin(pygame.time.get_ticks() * 0.015)
        wing_y = cy + 2 + int(wing_phase * 3)
        pygame.draw.ellipse(surf, settings.ORANGE,
                            (cx - self.radius + 3, wing_y, self.radius, 8))
        # eye
        pygame.draw.circle(surf, settings.WHITE, (cx + 6, cy - 5), 4)
        pygame.draw.circle(surf, settings.BLACK, (cx + 7, cy - 5), 2)
        # beak
        pygame.draw.polygon(surf, settings.ORANGE,
                            [(cx + self.radius - 2, cy),
                             (cx + self.radius + 6, cy + 2),
                             (cx + self.radius - 2, cy + 5)])
        rotated = pygame.transform.rotate(surf, -self.rotation)
        rect = rotated.get_rect(center=(int(self.x), int(self.y)))
        screen.blit(rotated, rect)