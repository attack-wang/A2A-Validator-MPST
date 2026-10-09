'''
effects.py
Short-lived visual effects. Explosion expands and fades over its duration
using a per-frame alpha-blended surface.
'''
import pygame
class Explosion:
    """An expanding, fading circle shown when an alien or the ship is destroyed."""
    def __init__(self, x, y, color, max_radius=24, duration=300):
        self.x, self.y = x, y
        self.color = color
        self.max_radius = max_radius
        self.duration = duration
        self.elapsed = 0
    def update(self, dt):
        """Advance the effect by dt ms. Return False when finished."""
        self.elapsed += dt
        return self.elapsed < self.duration
    def draw(self, screen):
        """Draw the expanding ring/circle with fading alpha."""
        progress = min(1.0, self.elapsed / self.duration)
        radius = max(2, int(self.max_radius * progress))
        alpha = int(255 * (1.0 - progress))
        surf = pygame.Surface((radius * 2, radius * 2), pygame.SRCALPHA)
        pygame.draw.circle(surf, (*self.color, alpha), (radius, radius), radius)
        screen.blit(surf, (self.x - radius, self.y - radius))