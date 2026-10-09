'''Bird entity: physics, wing animation, rotation, and rendering.'''
import pygame
from settings import (GRAVITY, FLAP_STRENGTH, MAX_FALL_SPEED)
from assets import create_bird_frames
class Bird:
    """The player-controlled bird with gravity, flapping, and tilt."""
    def __init__(self, x, y):
        """Build sprite frames and place the bird at its start position."""
        self.frames = create_bird_frames()
        self.reset(x, y)
    def reset(self, x, y):
        """Restore the bird to its initial flying state."""
        self.x = x
        self.y = y
        self.velocity = 0
        self.rotation = 0
        self.frame_index = 0
        self.animation_timer = 0
        self.alive = True
    def flap(self):
        """Apply an upward impulse; called on each flap input."""
        self.velocity = FLAP_STRENGTH
        self.rotation = -25  # snap upward so the tilt reads instantly
    def update(self, animate=True):
        """Advance physics, tilt, and wing animation by one frame."""
        # gravity accelerates the fall, capped at MAX_FALL_SPEED
        self.velocity = min(self.velocity + GRAVITY, MAX_FALL_SPEED)
        self.y += self.velocity
        # tilt up while rising, progressively nose-dive while falling
        if self.velocity < 0:
            target = -25
        else:
            target = min(90, self.rotation + 3)
        self.rotation += (target - self.rotation) * 0.15
        # wing flapping animation cycles through the three frames
        if animate:
            self.animation_timer += 1
            if self.animation_timer >= 5:
                self.animation_timer = 0
                self.frame_index = (self.frame_index + 1) % len(self.frames)
    def get_rect(self):
        """Return a collision box slightly smaller than the sprite."""
        return pygame.Rect(int(self.x) - 15, int(self.y) - 12, 30, 24)
    def draw(self, surface):
        """Blit the current animation frame rotated by the tilt angle."""
        frame = self.frames[self.frame_index]
        rotated = pygame.transform.rotate(frame, self.rotation)
        surface.blit(rotated, rotated.get_rect(center=(self.x, self.y)))