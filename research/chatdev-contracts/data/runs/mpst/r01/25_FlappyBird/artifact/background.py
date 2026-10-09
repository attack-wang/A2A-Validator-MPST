"""Scrolling background: parallax clouds and the ground strip."""
import random
import pygame
import settings
class Background:
    """Draws sky, drifting clouds, and a scrolling ground."""
    def __init__(self):
        self.ground_offset = 0.0
        self.clouds = []
        for _ in range(6):
            self.clouds.append({
                "x": random.uniform(0, settings.SCREEN_WIDTH),
                "y": random.uniform(40, settings.SCREEN_HEIGHT * 0.45),
                "scale": random.uniform(0.7, 1.5),
                "speed": random.uniform(0.15, 0.35),
            })
    def update(self, dt, world_speed):
        """Scroll the ground and clouds based on the world speed."""
        self.ground_offset = (self.ground_offset + world_speed * dt) % 48
        for cloud in self.clouds:
            cloud["x"] -= world_speed * cloud["speed"] * dt
            width = 90 * cloud["scale"]
            if cloud["x"] < -width:
                cloud["x"] = settings.SCREEN_WIDTH + random.uniform(0, 120)
                cloud["y"] = random.uniform(40, settings.SCREEN_HEIGHT * 0.45)
    def draw(self, surface):
        """Render sky gradient, clouds, and the ground."""
        surface.fill(settings.SKY_BLUE)
        for cloud in self.clouds:
            self._draw_cloud(surface, cloud["x"], cloud["y"], cloud["scale"])
        ground_top = settings.SCREEN_HEIGHT - settings.GROUND_HEIGHT
        pygame.draw.rect(surface, settings.GROUND_COLOR,
                         (0, ground_top, settings.SCREEN_WIDTH, settings.GROUND_HEIGHT))
        stripe_w = 24
        x = -int(self.ground_offset)
        while x < settings.SCREEN_WIDTH:
            pygame.draw.rect(surface, settings.GROUND_DARK, (x, ground_top, stripe_w, 12))
            x += stripe_w * 2
        pygame.draw.rect(surface, settings.GREEN, (0, ground_top, settings.SCREEN_WIDTH, 10))
        pygame.draw.rect(surface, settings.DARK_GREEN, (0, ground_top + 10, settings.SCREEN_WIDTH, 3))
    @staticmethod
    def _draw_cloud(surface, x, y, scale):
        """Draw a puffy cloud from overlapping ellipses."""
        r = int(18 * scale)
        for dx, dy, rr in ((0, 0, r), (-r, int(r * 0.3), int(r * 0.75)),
                           (r, int(r * 0.3), int(r * 0.75)),
                           (int(r * 0.4), -int(r * 0.5), int(r * 0.7))):
            pygame.draw.ellipse(surface, settings.CLOUD_COLOR,
                                (int(x + dx - rr), int(y + dy - rr * 0.7), rr * 2, int(rr * 1.4)))