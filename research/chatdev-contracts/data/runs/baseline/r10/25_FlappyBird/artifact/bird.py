'''
bird.py
The player-controlled bird.
Handles flap physics (gravity + impulse), rotation animation, wing flapping
and self-contained rendering so no external image assets are required.
'''
import math
import pygame
from settings import (
    GRAVITY, FLAP_STRENGTH, MAX_FALL_SPEED,
    BIRD_WIDTH, BIRD_HEIGHT, BIRD_HITBOX_SHRINK,
    MAX_ROTATION_UP, MAX_ROTATION_DOWN,
    BIRD_BODY, BIRD_WING, BIRD_BEAK, BIRD_EYE_WHITE, OUTLINE,
    SCREEN_HEIGHT, GROUND_HEIGHT,
)
class Bird:
    """Flappy bird: position, velocity, animation and drawing."""
    def __init__(self, x, y):
        self.x = float(x)
        self.y = float(y)
        self.velocity = 0.0
        self.rotation = 0.0
        self.wing_timer = 0
        self.alive = True
        self._surface = self._render(0)
    def flap(self):
        self.velocity = FLAP_STRENGTH
        self.wing_timer = 0
    def update(self):
        self.velocity = min(self.velocity + GRAVITY, MAX_FALL_SPEED)
        self.y += self.velocity
        if self.alive:
            # clamp at ceiling (classic behaviour: top does not kill)
            ceiling = BIRD_HEIGHT / 2
            if self.y < ceiling:
                self.y = ceiling
                if self.velocity < 0:
                    self.velocity = 0
            # rotation: nose up quickly when flapping, tip down while falling
            if self.velocity < 0:
                self.rotation = max(MAX_ROTATION_UP, self.rotation - 9)
            else:
                self.rotation = min(MAX_ROTATION_DOWN, self.rotation + 3.2)
            # wing flapping cycle
            self.wing_timer += 1
            cycle = self.wing_timer % 12
            if cycle < 4:
                wing_offset = -4
            elif cycle < 8:
                wing_offset = 0
            else:
                wing_offset = 4
        else:
            # dying: nose dive, wing limp
            self.rotation = min(MAX_ROTATION_DOWN, self.rotation + 6)
            wing_offset = -5
        self._surface = self._render(wing_offset)
    @property
    def hitbox(self):
        rect = pygame.Rect(0, 0, BIRD_WIDTH, BIRD_HEIGHT)
        rect.center = (int(self.x), int(self.y))
        return rect.inflate(-BIRD_HITBOX_SHRINK, -BIRD_HITBOX_SHRINK)
    def draw(self, surface):
        rotated = pygame.transform.rotate(self._surface, -self.rotation)
        surface.blit(rotated, rotated.get_rect(center=(int(self.x), int(self.y))))
    def _render(self, wing_offset):
        """Draw the bird onto an internal surface (no external assets)."""
        w, h = BIRD_WIDTH + 8, BIRD_HEIGHT + 8  # padding for beak/rotation
        surf = pygame.Surface((w, h), pygame.SRCALPHA)
        body_rect = pygame.Rect(4, 4, BIRD_WIDTH, BIRD_HEIGHT)
        # body
        pygame.draw.ellipse(surf, BIRD_BODY, body_rect)
        pygame.draw.ellipse(surf, OUTLINE, body_rect, 2)
        # wing (position depends on wing_offset)
        wing_rect = pygame.Rect(8, 14 + wing_offset, 16, 10)
        pygame.draw.ellipse(surf, BIRD_WING, wing_rect)
        pygame.draw.ellipse(surf, OUTLINE, wing_rect, 1)
        # eye
        eye_pos = (w - 16, 12)
        pygame.draw.circle(surf, BIRD_EYE_WHITE, eye_pos, 5)
        pygame.draw.circle(surf, OUTLINE, (eye_pos[0] + 2, eye_pos[1]), 2)
        # beak
        beak_points = [(w - 6, h // 2 - 3), (w - 6, h // 2 + 5), (w + 2, h // 2 + 1)]
        pygame.draw.polygon(surf, BIRD_BEAK, beak_points)
        return surf