'''
bird.py
Defines the Bird class: the player-controlled character.
The bird is affected by constant gravity; pressing the flap key gives it
an upward velocity. The sprite is drawn procedurally (no image assets
required) with a three-frame wing animation and velocity-based rotation.
update_dead() implements the post-crash tumble and reports when the bird
has come to rest on the ground so the game can switch to GAME_OVER.
'''
import math
import pygame
import settings
class Bird:
    """Player-controlled bird with gravity, flapping and animation."""
    FRAME_DURATION = 0.09  # seconds per wing-animation frame
    TOP_MARGIN = 12        # bird may not fly above this sky line
    def __init__(self, x, y):
        self.x = float(x)
        self.y = float(y)
        self.velocity = 0.0
        self.rotation = 0.0
        self.frames = self._build_frames()
        self.frame_index = 0
        self.frame_timer = 0.0
        self.alive = True
        self.rect = self.frames[0].get_rect(center=(int(self.x), int(self.y)))
    # ---------------------------------------------------------------- art
    @staticmethod
    def _build_frames():
        """Create the three wing-animation frames procedurally."""
        width, height = 40, 30
        frames = []
        wing_offsets = (-4, 0, 4)  # wing up / middle / down
        for offset in wing_offsets:
            frame = pygame.Surface((width, height), pygame.SRCALPHA)
            body_rect = pygame.Rect(2, 4, 30, 22)
            # body
            pygame.draw.ellipse(frame, settings.BIRD_YELLOW, body_rect)
            pygame.draw.ellipse(frame, settings.BIRD_OUTLINE, body_rect, 2)
            # belly highlight
            pygame.draw.ellipse(frame, settings.BIRD_LIGHT, pygame.Rect(8, 16, 18, 8))
            # wing
            wing = pygame.Rect(8, 12 + offset, 14, 8)
            pygame.draw.ellipse(frame, settings.BIRD_WING, wing)
            pygame.draw.ellipse(frame, settings.BIRD_OUTLINE, wing, 1)
            # eye
            pygame.draw.circle(frame, (255, 255, 255), (26, 10), 5)
            pygame.draw.circle(frame, (30, 30, 30), (28, 10), 2)
            # beak
            pygame.draw.polygon(frame, settings.BIRD_BEAK, [(30, 13), (40, 16), (30, 19)])
            pygame.draw.polygon(frame, settings.BIRD_OUTLINE, [(30, 13), (40, 16), (30, 19)], 1)
            frames.append(frame)
        return frames
    # ------------------------------------------------------------ control
    def flap(self):
        """Give the bird an upward impulse (only while alive)."""
        if self.alive:
            self.velocity = settings.FLAP_VELOCITY
    def reset(self, x, y):
        """Restore the bird to its starting state for a new round."""
        self.x = float(x)
        self.y = float(y)
        self.velocity = 0.0
        self.rotation = 0.0
        self.frame_index = 0
        self.frame_timer = 0.0
        self.alive = True
        self.rect.center = (int(self.x), int(self.y))
    # ------------------------------------------------------------- physics
    def update(self, dt):
        """Apply gravity, smooth rotation and advance the wing animation."""
        self.velocity = min(self.velocity + settings.GRAVITY * dt,
                            settings.MAX_FALL_SPEED)
        self.y += self.velocity * dt
        # keep the bird from leaving the top of the sky
        if self.y < self.TOP_MARGIN:
            self.y = self.TOP_MARGIN
            if self.velocity < 0:
                self.velocity = 0.0
        # Rotation: tilt up while flapping, nose-dive as fall speed grows.
        if self.velocity < 0:
            target = 25.0
        else:
            target = max(-90.0, 25.0 - (self.velocity / settings.MAX_FALL_SPEED) * 115.0)
        self.rotation += (target - self.rotation) * min(1.0, dt * 12.0)
        self.update_animation(dt)
        self.rect.center = (int(self.x), int(self.y))
    def update_dead(self, dt):
        """Tumble to the ground after a fatal collision.
        Returns True once the bird has come to rest on the ground so the
        caller can transition to the GAME_OVER state.
        """
        self.velocity = min(self.velocity + settings.GRAVITY * dt,
                            settings.MAX_FALL_SPEED)
        self.y += self.velocity * dt
        landed = False
        rest_y = settings.SKY_HEIGHT - 10
        if self.y >= rest_y:
            self.y = rest_y
            landed = True
        self.rotation = max(-90.0, self.rotation - 360.0 * dt)
        self.rect.center = (int(self.x), int(self.y))
        return landed
    def update_animation(self, dt):
        """Cycle through the wing frames while alive."""
        self.frame_timer += dt
        if self.frame_timer >= self.FRAME_DURATION:
            self.frame_timer = 0.0
            self.frame_index = (self.frame_index + 1) % len(self.frames)
    # ---------------------------------------------------------- collision
    def get_collision_rect(self):
        """Slightly forgiving hitbox (smaller than the sprite)."""
        rect = pygame.Rect(0, 0, 26, 20)
        rect.center = (int(self.x), int(self.y))
        return rect
    # -------------------------------------------------------------- draw
    def draw(self, surface):
        """Blit the current frame rotated by the current angle."""
        frame = self.frames[self.frame_index]
        rotated = pygame.transform.rotate(frame, self.rotation)
        surface.blit(rotated, rotated.get_rect(center=(int(self.x), int(self.y))))