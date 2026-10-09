'''
Bird entity: physics, flapping, and rendering.
'''
import pygame
import settings
class Bird:
    '''Represents the player-controlled bird with gravity physics.'''
    def __init__(self, x, y):
        '''Initialize bird position, velocity, rotation, and animation timers.'''
        self.x = x
        self.y = y
        self.velocity = 0.0
        self.rotation = 0.0
        self.wing_frame = 0.0  # animation timer
        self.flap_animation = 0.0
    def flap(self):
        '''Apply an upward impulse to counteract gravity.'''
        self.velocity = settings.FLAP_VELOCITY
        self.flap_animation = 0.25  # wing flap animation duration
    def update(self, dt):
        '''Apply gravity and integrate position; update rotation/animation.'''
        self.velocity += settings.GRAVITY * dt
        if self.velocity > settings.MAX_FALL_SPEED:
            self.velocity = settings.MAX_FALL_SPEED
        self.y += self.velocity * dt
        # Clamp to ceiling (bird cannot fly above the screen)
        if self.y < settings.BIRD_RADIUS:
            self.y = settings.BIRD_RADIUS
            self.velocity = max(self.velocity, 0.0)
        # Rotation: tilt up when flapping, nose-dive when falling
        target_rotation = max(-25, min(90, self.velocity / 6.0))
        self.rotation += (target_rotation - self.rotation) * min(1.0, dt * 10)
        # Wing animation timer
        if self.flap_animation > 0:
            self.flap_animation -= dt
        self.wing_frame += dt
    def get_rect(self):
        '''Return the collision rectangle for the bird body.'''
        return pygame.Rect(
            int(self.x - settings.BIRD_RADIUS),
            int(self.y - settings.BIRD_RADIUS),
            settings.BIRD_RADIUS * 2,
            settings.BIRD_RADIUS * 2,
        )
    def draw(self, screen):
        '''Render the bird as a stylized shape with rotation.'''
        # draw with rotation using a surface
        size = settings.BIRD_RADIUS * 3
        surf = pygame.Surface((size, size), pygame.SRCALPHA)
        center = size // 2
        r = settings.BIRD_RADIUS
        # body
        pygame.draw.circle(surf, settings.BIRD_YELLOW, (center, center), r)
        pygame.draw.circle(surf, settings.BIRD_ORANGE, (center, center), r, 2)
        # eye
        pygame.draw.circle(surf, settings.WHITE, (center + r // 2, center - r // 3), r // 3)
        pygame.draw.circle(surf, settings.BLACK,
                           (center + r // 2 + 1, center - r // 3), max(1, r // 6))
        # beak
        pygame.draw.polygon(surf, settings.BIRD_ORANGE, [
            (center + r - 2, center),
            (center + r + 8, center + 2),
            (center + r - 2, center + 6),
        ])
        # wing (animated)
        wing_y = center
        if self.flap_animation > 0:
            wing_y = center - r // 2
        elif self.velocity > 200:
            wing_y = center + r // 3
        pygame.draw.ellipse(surf, settings.BIRD_ORANGE,
                            (center - r + 2, wing_y - 3, r, 7))
        # rotate and blit
        rotated = pygame.transform.rotate(surf, -self.rotation)
        rect = rotated.get_rect(center=(int(self.x), int(self.y)))
        screen.blit(rotated, rect)