"""
ground.py
The scrolling ground strip at the bottom of the screen.
Renders a dirt block with a grass top edge and a repeating diagonal
pattern that scrolls to sell the sense of speed. Also provides the
collision surface the bird must never touch.
"""
import pygame
import settings
class Ground:
    """Scrolling ground: dirt block + grass strip + diagonal stripes."""
    STRIPE_SPACING = 24  # horizontal distance between diagonal stripes
    def __init__(self):
        self.y = settings.SCREEN_HEIGHT - settings.GROUND_HEIGHT
        self.offset = 0.0
        self.pattern_width = self.STRIPE_SPACING * 2
    def update(self, speed):
        self.offset = (self.offset + speed) % self.pattern_width
    def get_rect(self):
        return pygame.Rect(0, self.y, settings.SCREEN_WIDTH, settings.GROUND_HEIGHT)
    def collide(self, rect):
        return rect.colliderect(self.get_rect())
    def draw(self, surface):
        # Dirt body
        pygame.draw.rect(surface, settings.GROUND_DIRT, self.get_rect())
        # Grass strip
        grass_rect = pygame.Rect(0, self.y, settings.SCREEN_WIDTH, 22)
        pygame.draw.rect(surface, settings.GRASS, grass_rect)
        pygame.draw.rect(surface, settings.GRASS_DARK, grass_rect, 3)
        # Light edge line on top of the grass
        pygame.draw.line(surface, settings.GRASS_EDGE, (0, self.y + 1),
                         (settings.SCREEN_WIDTH, self.y + 1), 2)
        # Diagonal pattern on the dirt
        stripe_color = settings.GROUND_DIRT_DARK
        start = -self.pattern_width + int(self.offset)
        x = start
        while x < settings.SCREEN_WIDTH + self.pattern_width:
            pygame.draw.line(surface, stripe_color,
                             (x, self.y + grass_rect.height),
                             (x + 18, settings.SCREEN_HEIGHT), 6)
            x += self.STRIPE_SPACING