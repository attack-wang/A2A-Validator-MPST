'''
Bird entity: physics, animation, and collision helpers.
'''
import math
import pygame
import settings
from utils import clamp
class Bird:
    def __init__(self, x, y):
        self.start_x = x
        self.start_y = y
        self.radius = settings.BIRD_RADIUS
        self.reset()
    def reset(self):
        self.x = float(self.start_x)
        self.y = float(self.start_y)
        self.velocity = 0.0
        self.rotation = 0.0
        self.flap_animation = 0.0
        self.anim_time = 0.0
        self._build_image()
    def flap(self):
        self.velocity = settings.FLAP_VELOCITY
        self.flap_animation = 0.25
    def update(self, dt):
        self.velocity = min(self.velocity + settings.GRAVITY * dt, settings.MAX_FALL_SPEED)
        self.y += self.velocity * dt
        if self.y < self.radius:
            self.y = self.radius
            self.velocity = 0.0
        target = clamp(self.velocity * 0.12, -28.0, 90.0)
        self.rotation += (target - self.rotation) * min(1.0, dt * 12)
        if self.flap_animation > 0:
            self.flap_animation = max(0.0, self.flap_animation - dt)
        self.anim_time += dt
    def get_collision_circle(self):
        return (self.x, self.y, self.radius * 0.9)
    def hits_rect(self, rect):
        cx, cy, r = self.get_collision_circle()
        nearest_x = clamp(cx, rect.left, rect.right)
        nearest_y = clamp(cy, rect.top, rect.bottom)
        dx = cx - nearest_x
        dy = cy - nearest_y
        return dx * dx + dy * dy < r * r
    def _build_image(self):
        r = self.radius
        size = int(r * 2 + 10)
        surf = pygame.Surface((size, size), pygame.SRCALPHA)
        cx = size // 2
        cy = size // 2
        # body
        pygame.draw.circle(surf, settings.BIRD_YELLOW, (cx, cy), r)
        pygame.draw.circle(surf, settings.BIRD_OUTLINE, (cx, cy), r, 2)
        # belly
        pygame.draw.ellipse(surf, settings.BIRD_BELLY, (cx - r + 3, cy + 1, r * 2 - 8, r - 3))
        # wing (animated up/down based on flap animation)
        wing_up = self.flap_animation > 0 or (math.sin(self.anim_time * 10) > 0)
        wing_y = cy - 5 if wing_up else cy + 2
        wing_rect = pygame.Rect(cx - r - 1, wing_y, r, max(5, r - 4))
        pygame.draw.ellipse(surf, settings.BIRD_WING, wing_rect)
        pygame.draw.ellipse(surf, settings.BIRD_OUTLINE, wing_rect, 1)
        # eye
        pygame.draw.circle(surf, settings.WHITE, (cx + int(r * 0.45), cy - int(r * 0.35)), max(2, int(r * 0.42)))
        pygame.draw.circle(surf, settings.BLACK, (cx + int(r * 0.55), cy - int(r * 0.35)), max(1, int(r * 0.18)))
        # beak
        pygame.draw.polygon(surf, settings.BEAK_ORANGE, [
            (cx + r * 0.6, cy - 2),
            (cx + r * 1.5, cy),
            (cx + r * 0.6, cy + 6),
        ])
        self.image = surf
    def draw(self, surface):
        rotated = pygame.transform.rotate(self.image, -self.rotation)
        rect = rotated.get_rect(center=(int(self.x), int(self.y)))
        surface.blit(rotated, rect)