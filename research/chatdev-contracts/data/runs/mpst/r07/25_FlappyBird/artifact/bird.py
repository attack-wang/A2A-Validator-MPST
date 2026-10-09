"""
bird.py
The Bird entity: physics, animation and rendering.
The bird is drawn procedurally (no image assets) onto a small off-screen
surface which is then rotated according to the current vertical velocity,
mimicking the tilting of the original Flappy Bird.
"""
import math
import pygame
import settings
class Bird:
    """Player-controlled bird with gravity physics and procedural graphics."""
    def __init__(self, x, y):
        self.x = float(x)
        self.y = float(y)
        self.velocity = 0.0
        self.rotation = 0.0
        self.anim_timer = 0.0
        self.flap_anim = 0          # frames of accelerated wing flapping left
        self._sprite = self._build_sprite()
    # ------------------------------------------------------------------ physics
    def flap(self):
        """Apply an instantaneous upward impulse."""
        self.velocity = settings.FLAP_STRENGTH
        self.flap_anim = 10
    def update(self):
        """Advance one physics frame: gravity, position, tilt, animation."""
        self.velocity = min(self.velocity + settings.GRAVITY, settings.MAX_FALL_SPEED)
        self.y += self.velocity
        # The bird may not leave the sky through the top; it simply stalls.
        if self.y < settings.BIRD_RADIUS:
            self.y = settings.BIRD_RADIUS
            self.velocity = max(self.velocity, 0.0)
        # Tilt: nose up shortly after a flap, nose diving while falling.
        if self.velocity < 0:
            target = 28.0
        else:
            target = max(-90.0, -(self.velocity - 2) * 9.0)
        self.rotation += (target - self.rotation) * 0.25
        # Wing animation runs faster for a few frames after each flap.
        speed = 0.55 if self.flap_anim > 0 else 0.18
        self.anim_timer += speed
        if self.flap_anim > 0:
            self.flap_anim -= 1
    def get_collision_rect(self):
        """Slightly forgiving hitbox (smaller than the visual sprite)."""
        return pygame.Rect(
            int(self.x - 13), int(self.y - 10), 26, 20
        )
    def hits_ground(self):
        return self.y + 10 >= settings.SCREEN_HEIGHT - settings.GROUND_HEIGHT
    # ------------------------------------------------------------------ drawing
    def _build_sprite(self):
        """Pre-render the (unrotated) bird onto an off-screen surface."""
        width, height = 68, 44
        surface = pygame.Surface((width, height), pygame.SRCALPHA)
        cx, cy = 30, 22  # body centre inside the sprite
        # Body
        pygame.draw.ellipse(surface, settings.BIRD_BODY, (cx - 20, cy - 15, 40, 30))
        pygame.draw.ellipse(surface, settings.BIRD_BODY_DARK, (cx - 20, cy - 15, 40, 30), 2)
        # Belly
        pygame.draw.ellipse(surface, settings.BIRD_BELLY, (cx - 12, cy + 2, 24, 12))
        # Beak (drawn before the eye so the eye overlaps its top edge)
        pygame.draw.polygon(surface, settings.BEAK,
                            [(cx + 14, cy - 3), (cx + 30, cy + 1), (cx + 14, cy + 7)])
        pygame.draw.polygon(surface, settings.BEAK_DARK,
                            [(cx + 14, cy + 3), (cx + 30, cy + 1), (cx + 14, cy + 7)], 1)
        # Eye
        pygame.draw.circle(surface, settings.EYE_WHITE, (cx + 10, cy - 7), 6)
        pygame.draw.circle(surface, settings.EYE_BLACK, (cx + 12, cy - 7), 3)
        return surface
    def draw(self, surface):
        """Blit the bird, rotating the pre-rendered sprite by current tilt."""
        # Wing is drawn dynamically so it can animate.
        sprite = self._sprite.copy()
        wing_offset = int(math.sin(self.anim_timer) * 4)
        wing_rect = pygame.Rect(6, 20 + wing_offset, 20, 12)
        pygame.draw.ellipse(sprite, settings.BIRD_WING, wing_rect)
        pygame.draw.ellipse(sprite, settings.BIRD_BODY_DARK, wing_rect, 1)
        rotated = pygame.transform.rotate(sprite, self.rotation)
        rect = rotated.get_rect(center=(int(self.x), int(self.y)))
        surface.blit(rotated, rect.topleft)