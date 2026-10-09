'''
Scrolling background: sky gradient, clouds, and animated ground.
'''
import random
import pygame
import settings
class Background:
    """Draws the sky, drifting clouds, and a scrolling ground strip."""
    def __init__(self):
        self.ground_offset = 0.0
        self.clouds = self._make_clouds()
        self._sky = self._make_sky()
    def _make_sky(self):
        """Pre-render a vertical sky gradient surface."""
        sky = pygame.Surface((settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT - settings.GROUND_HEIGHT))
        top = settings.SKY_TOP
        bottom = settings.SKY_BOTTOM
        height = sky.get_height()
        for y in range(height):
            t = y / max(1, height - 1)
            color = (
                int(top[0] + (bottom[0] - top[0]) * t),
                int(top[1] + (bottom[1] - top[1]) * t),
                int(top[2] + (bottom[2] - top[2]) * t),
            )
            pygame.draw.line(sky, color, (0, y), (settings.SCREEN_WIDTH, y))
        return sky
    def _make_clouds(self):
        """Create a handful of slow-drifting cloud blobs."""
        clouds = []
        for _ in range(5):
            clouds.append({
                "x": random.uniform(0, settings.SCREEN_WIDTH),
                "y": random.uniform(40, settings.SCREEN_HEIGHT * 0.45),
                "speed": random.uniform(8, 20),
                "scale": random.uniform(0.7, 1.4),
            })
        return clouds
    def update(self, dt, speed):
        """Scroll the ground and drift the clouds."""
        self.ground_offset = (self.ground_offset + speed * settings.GROUND_SPEED_FACTOR * dt) % 24
        for cloud in self.clouds:
            cloud["x"] -= cloud["speed"] * dt
            if cloud["x"] < -80 * cloud["scale"]:
                cloud["x"] = settings.SCREEN_WIDTH + 40
                cloud["y"] = random.uniform(40, settings.SCREEN_HEIGHT * 0.45)
    def draw(self, surface):
        """Render sky, clouds, and ground."""
        surface.blit(self._sky, (0, 0))
        for cloud in self.clouds:
            self._draw_cloud(surface, cloud["x"], cloud["y"], cloud["scale"])
        self._draw_ground(surface)
    def _draw_cloud(self, surface, x, y, scale):
        """Draw a puffy cloud from overlapping circles."""
        r = int(18 * scale)
        color = settings.CLOUD_COLOR
        pygame.draw.circle(surface, color, (int(x), int(y)), r)
        pygame.draw.circle(surface, color, (int(x + r * 0.9), int(y + r * 0.2)), int(r * 0.75))
        pygame.draw.circle(surface, color, (int(x - r * 0.9), int(y + r * 0.25)), int(r * 0.7))
        pygame.draw.circle(surface, color, (int(x + r * 0.3), int(y - r * 0.5)), int(r * 0.65))
    def _draw_ground(self, surface):
        """Draw the grass edge and striped dirt ground."""
        ground_top = settings.SCREEN_HEIGHT - settings.GROUND_HEIGHT
        pygame.draw.rect(surface, settings.GRASS_COLOR, (0, ground_top, settings.SCREEN_WIDTH, 14))
        pygame.draw.rect(surface, settings.GROUND_COLOR, (0, ground_top + 14, settings.SCREEN_WIDTH, settings.GROUND_HEIGHT - 14))
        # Diagonal stripes for a scrolling effect
        stripe_w = 12
        gap_w = 12
        period = stripe_w + gap_w
        x = -int(self.ground_offset)
        while x < settings.SCREEN_WIDTH:
            pygame.draw.polygon(surface, settings.GROUND_DARK, [
                (x, ground_top + 14),
                (x + stripe_w, ground_top + 14),
                (x + stripe_w - 8, settings.SCREEN_HEIGHT),
                (x - 8, settings.SCREEN_HEIGHT),
            ])
            x += period
        pygame.draw.line(surface, settings.GRASS_EDGE, (0, ground_top), (settings.SCREEN_WIDTH, ground_top), 3)