import pygame
import settings
class Ground:
    def __init__(self, ground_y):
        self.ground_y = ground_y
        self.scroll_x = 0.0
    def update(self, dt, speed):
        self.scroll_x = (self.scroll_x + speed * dt) % settings.STRIPE_WIDTH
    def top(self):
        return self.ground_y
    def draw(self, surface):
        rect_top = self.ground_y
        height = settings.HEIGHT - rect_top
        # dirt base
        pygame.draw.rect(surface, settings.DIRT, (0, rect_top, settings.WIDTH, height))
        # grass strip
        grass_h = 22
        pygame.draw.rect(surface, settings.GRASS_GREEN, (0, rect_top, settings.WIDTH, grass_h))
        # diagonal stripes on grass
        stripe = settings.STRIPE_WIDTH
        offset = int(self.scroll_x)
        for x in range(-stripe, settings.WIDTH + stripe, stripe * 2):
            p1 = (x + offset, rect_top)
            p2 = (x + offset + stripe, rect_top)
            p3 = (x + offset + stripe - grass_h, rect_top + grass_h)
            p4 = (x + offset - grass_h, rect_top + grass_h)
            pygame.draw.polygon(surface, settings.GRASS_DARK, [p1, p2, p3, p4])
        # dark top edge
        pygame.draw.line(surface, settings.GRASS_DARK, (0, rect_top), (settings.WIDTH, rect_top), 2)
        # dirt darker bottom
        pygame.draw.rect(surface, settings.DIRT_DARK, (0, rect_top + grass_h, settings.WIDTH, height - grass_h))