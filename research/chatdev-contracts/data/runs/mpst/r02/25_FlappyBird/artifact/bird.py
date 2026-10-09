'''
Bird class: the player-controlled character.
'''
import pygame
import settings
class Bird:
    """Represents the flappy bird, handling physics, animation and drawing."""
    def __init__(self, x, y):
        self.start_x = x
        self.start_y = y
        self.reset()
    def reset(self):
        self.x = self.start_x
        self.y = self.start_y
        self.velocity = 0.0
        self.rotation = 0.0
        self.wing_timer = 0
        self.wing_frame = 0
        self.alive = True
    def flap(self):
        """Give the bird an upward impulse."""
        self.velocity = settings.FLAP_STRENGTH
        self.wing_timer = 0  # reset wing flap animation
    def update(self):
        """Apply gravity, move the bird, update rotation and wing animation."""
        self.velocity = min(self.velocity + settings.GRAVITY, settings.MAX_FALL_SPEED)
        self.y += self.velocity
        # Keep the bird inside the top of the window (touching the top is safe).
        if self.y - settings.BIRD_RADIUS < 0:
            self.y = settings.BIRD_RADIUS
            self.velocity = 0
        # Rotate: tilt up quickly when flapping, rotate down while falling.
        if self.velocity < 0:
            self.rotation = max(-settings.MAX_ROTATION_UP,
                                self.rotation - settings.ROTATION_SPEED_UP * 2)
        else:
            self.rotation = min(settings.MAX_ROTATION_DOWN,
                                self.rotation + settings.ROTATION_SPEED_DOWN)
        # Wing flapping animation cycles faster right after a flap.
        self.wing_timer += 1
        if self.velocity < 0:
            self.wing_frame = (self.wing_timer // 3) % 4
        else:
            self.wing_frame = (self.wing_timer // 8) % 4
    def get_rect(self):
        """Return the collision rectangle (slightly smaller than the sprite)."""
        r = settings.BIRD_RADIUS - 2
        return pygame.Rect(int(self.x - r), int(self.y - r), r * 2, r * 2)
    def _build_sprite(self):
        """Draw the bird onto a local surface so it can be rotated."""
        size = settings.BIRD_RADIUS * 3
        surface = pygame.Surface((size, size), pygame.SRCALPHA)
        cx = cy = size // 2
        r = settings.BIRD_RADIUS
        # Body
        pygame.draw.circle(surface, settings.BIRD_BODY, (cx, cy), r)
        # Wing (position depends on animation frame)
        wing_offsets = [-4, -2, 1, -2]
        wy = cy + wing_offsets[self.wing_frame]
        pygame.draw.ellipse(surface, settings.BIRD_WING, (cx - r + 2, wy - 4, r + 2, 9))
        # Eye
        eye_x = cx + r // 2
        eye_y = cy - r // 2 + 1
        pygame.draw.circle(surface, settings.BIRD_EYE, (eye_x, eye_y), 5)
        pygame.draw.circle(surface, settings.BIRD_PUPIL, (eye_x + 2, eye_y), 2)
        # Beak
        beak_rect = pygame.Rect(cx + r - 4, cy - 1, 10, 7)
        pygame.draw.polygon(surface, settings.BIRD_BEAK,
                            [(beak_rect.left, beak_rect.top),
                             (beak_rect.right, beak_rect.centery),
                             (beak_rect.left, beak_rect.bottom)])
        return surface
    def draw(self, surface):
        """Draw the rotated bird at its current position."""
        sprite = self._build_sprite()
        rotated = pygame.transform.rotate(sprite, -self.rotation)
        rect = rotated.get_rect(center=(int(self.x), int(self.y)))
        surface.blit(rotated, rect.topleft)