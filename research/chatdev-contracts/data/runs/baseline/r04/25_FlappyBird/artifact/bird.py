'''
Bird entity: physics, flapping, rotation and drawing.
'''
import math
import pygame
import settings
class Bird:
    '''Represents the player-controlled bird with simple gravity physics.'''
    def __init__(self, x, y):
        self.start_x = x
        self.start_y = y
        self.reset()
    def reset(self):
        self.x = self.start_x
        self.y = self.start_y
        self.velocity = 0.0
        self.rotation = 0.0
        self.wing_frame = 0
        self.alive = True
    def flap(self):
        '''Give the bird an upward impulse.'''
        self.velocity = settings.FLAP_STRENGTH
        self.wing_frame = 6  # wing animation timer
    def update(self):
        '''Apply gravity and update position/rotation each frame.'''
        self.velocity = min(self.velocity + settings.GRAVITY, settings.MAX_FALL_SPEED)
        self.y += self.velocity
        # Rotation: tilt up quickly on flap, slowly rotate down while falling
        target = -25 if self.velocity < 0 else min(90, self.velocity * 7)
        self.rotation += (target - self.rotation) * 0.15
        if self.wing_frame > 0:
            self.wing_frame -= 1
    @property
    def rect(self):
        '''Collision rectangle (slightly smaller than the sprite for fairness).'''
        r = settings.BIRD_RADIUS
        return pygame.Rect(self.x - r + 3, self.y - r + 3, (r - 3) * 2, (r - 3) * 2)
    def draw(self, surface):
        '''Draw the bird as composed shapes, rotated with its velocity.'''
        r = settings.BIRD_RADIUS
        bird_surface = pygame.Surface((r * 3, r * 3), pygame.SRCALPHA)
        cx = cy = r * 1.5
        # body
        pygame.draw.ellipse(bird_surface, settings.BIRD_BODY,
                            (cx - r, cy - r * 0.8, r * 2, r * 1.6))
        # wing (flaps up/down)
        wing_offset = -4 if self.wing_frame > 0 else 2
        pygame.draw.ellipse(bird_surface, settings.BIRD_WING,
                            (cx - r * 0.9, cy + wing_offset, r * 1.1, r * 0.7))
        # eye
        pygame.draw.circle(bird_surface, settings.WHITE,
                           (int(cx + r * 0.45), int(cy - r * 0.35)), 5)
        pygame.draw.circle(bird_surface, settings.BIRD_EYE,
                           (int(cx + r * 0.55), int(cy - r * 0.35)), 2)
        # beak
        pygame.draw.polygon(bird_surface, settings.BIRD_BEAK,
                            [(cx + r * 0.8, cy - 3), (cx + r * 1.5, cy + 2), (cx + r * 0.8, cy + 6)])
        # rotate
        rotated = pygame.transform.rotate(bird_surface, -self.rotation)
        rect = rotated.get_rect(center=(self.x, self.y))
        surface.blit(rotated, rect)