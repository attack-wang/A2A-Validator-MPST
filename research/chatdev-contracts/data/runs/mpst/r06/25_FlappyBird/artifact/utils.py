'''
utils.py
Background scenery: vertical sky gradient, drifting clouds and a
scrolling ground strip. Purely cosmetic — contains no gameplay logic.
'''
import random
import pygame
from settings import (
    SCREEN_WIDTH, SCREEN_HEIGHT, GROUND_HEIGHT,
    SKY_TOP, SKY_BOTTOM, CLOUD_WHITE,
    GROUND_GREEN, GROUND_DIRT, GROUND_GRASS,
    GROUND_TILE_WIDTH,
)
class Background:
    """Animates and renders sky, clouds and ground behind the gameplay."""
    def __init__(self):
        self._sky = self._build_sky()
        self.clouds = self._make_clouds()
        self.ground_offset = 0.0
    # ------------------------------------------------------------------ #
    # Setup helpers
    # ------------------------------------------------------------------ #
    def _build_sky(self):
        """Pre-render the vertical sky gradient once for performance."""
        sky = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        for y in range(SCREEN_HEIGHT):
            t = y / max(1, SCREEN_HEIGHT - 1)
            colour = tuple(
                int(top + (bottom - top) * t)
                for top, bottom in zip(SKY_TOP, SKY_BOTTOM)
            )
            pygame.draw.line(sky, colour, (0, y), (SCREEN_WIDTH, y))
        return sky
    def _make_clouds(self):
        """Create a scattered set of clouds with random drift speeds."""
        return [
            {
                "x": random.uniform(0, SCREEN_WIDTH),
                "y": random.uniform(40, SCREEN_HEIGHT * 0.45),
                "scale": random.uniform(0.7, 1.6),
                "speed": random.uniform(0.15, 0.45),
            }
            for _ in range(6)
        ]
    def reset(self):
        """Re-randomise the scenery when a new run begins."""
        self.clouds = self._make_clouds()
        self.ground_offset = 0.0
    # ------------------------------------------------------------------ #
    # Animation
    # ------------------------------------------------------------------ #
    def update(self, speed):
        """Drift the clouds slowly and scroll the ground with pipe speed."""
        for cloud in self.clouds:
            cloud["x"] -= cloud["speed"]
            if cloud["x"] < -140 * cloud["scale"]:
                cloud["x"] = SCREEN_WIDTH + random.uniform(0, 140)
                cloud["y"] = random.uniform(40, SCREEN_HEIGHT * 0.45)
        self.ground_offset = (self.ground_offset - speed) % GROUND_TILE_WIDTH
    # ------------------------------------------------------------------ #
    # Rendering
    # ------------------------------------------------------------------ #
    def _draw_cloud(self, surface, x, y, scale):
        """Draw one puffy cloud built from three overlapping circles."""
        r = int(18 * scale)
        pygame.draw.circle(surface, CLOUD_WHITE, (int(x), int(y)), r)
        pygame.draw.circle(surface, CLOUD_WHITE,
                           (int(x + r * 0.9), int(y + r * 0.2)), int(r * 0.75))
        pygame.draw.circle(surface, CLOUD_WHITE,
                           (int(x - r * 0.9), int(y + r * 0.25)), int(r * 0.65))
    def _draw_ground(self, surface):
        """Draw the grass strip with diagonal dirt stripes for scrolling."""
        ground_top = SCREEN_HEIGHT - GROUND_HEIGHT
        pygame.draw.rect(surface, GROUND_GRASS,
                         (0, ground_top, SCREEN_WIDTH, 14))
        pygame.draw.rect(surface, GROUND_GREEN,
                         (0, ground_top + 14, SCREEN_WIDTH, GROUND_HEIGHT - 14))
        stripe = GROUND_TILE_WIDTH
        x = -stripe * 2 + self.ground_offset
        while x < SCREEN_WIDTH:
            pygame.draw.polygon(surface, GROUND_DIRT, [
                (x, ground_top + 14),
                (x + stripe // 2, ground_top + 14),
                (x + stripe // 2 - 8, SCREEN_HEIGHT),
                (x - 8, SCREEN_HEIGHT),
            ])
            x += stripe * 2
        pygame.draw.line(surface, GROUND_DIRT,
                         (0, ground_top + 14), (SCREEN_WIDTH, ground_top + 14), 2)
    def draw(self, surface):
        """Blit sky, clouds and ground in back-to-front order."""
        surface.blit(self._sky, (0, 0))
        for cloud in self.clouds:
            self._draw_cloud(surface, cloud["x"], cloud["y"], cloud["scale"])
        self._draw_ground(surface)