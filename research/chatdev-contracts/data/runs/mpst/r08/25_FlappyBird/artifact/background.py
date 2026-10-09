'''
Parallax background: gradient sky, drifting clouds and scrolling ground.
'''
import random
import pygame
import settings
class Background:
    """Draws the sky, clouds and scrolling ground; owns no game logic."""
    def __init__(self):
        self._build_sky()
        self._build_ground()
        self.clouds = []
        for _ in range(5):
            self.clouds.append({
                'x': random.uniform(0, settings.SCREEN_WIDTH),
                'y': random.uniform(40, settings.SCREEN_HEIGHT * 0.45),
                'speed': random.uniform(8.0, 20.0),
                'scale': random.uniform(0.7, 1.4),
            })
        self.ground_offset = 0.0
    def _build_sky(self):
        """Pre-render the vertical sky gradient once."""
        sky = pygame.Surface((settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT))
        top = settings.SKY_TOP
        bottom = settings.SKY_BOTTOM
        for y in range(settings.SCREEN_HEIGHT):
            t = y / (settings.SCREEN_HEIGHT - 1)
            color = (int(top[0] + (bottom[0] - top[0]) * t),
                     int(top[1] + (bottom[1] - top[1]) * t),
                     int(top[2] + (bottom[2] - top[2]) * t))
            pygame.draw.line(sky, color, (0, y), (settings.SCREEN_WIDTH, y))
        self.sky_surface = sky
    def _build_ground(self):
        """Pre-render the ground tile (grass strip + dirt stripes)."""
        w = settings.SCREEN_WIDTH
        h = settings.GROUND_HEIGHT
        ground = pygame.Surface((w, h))
        ground.fill(settings.GROUND_COLOR)
        pygame.draw.rect(ground, settings.GRASS_LIGHT, (0, 0, w, 12))
        pygame.draw.rect(ground, settings.GRASS_DARK, (0, 12, w, 4))
        for x in range(0, w, 40):
            pygame.draw.rect(ground, settings.GROUND_DARK, (x, 30, 20, h - 30))
        self.ground_surface = ground
    def update(self, dt, speed):
        """Drift clouds and scroll the ground at the given world speed."""
        for c in self.clouds:
            c['x'] -= (c['speed'] + speed * 0.05) * dt
            if c['x'] < -80:
                c['x'] = settings.SCREEN_WIDTH + random.uniform(0, 80)
                c['y'] = random.uniform(40, settings.SCREEN_HEIGHT * 0.45)
        self.ground_offset = (self.ground_offset + speed * dt) % 40
    def draw(self, screen):
        """Blit sky, clouds and the twice-tiled scrolling ground."""
        screen.blit(self.sky_surface, (0, 0))
        for c in self.clouds:
            self._draw_cloud(screen, c['x'], c['y'], c['scale'])
        ground_y = settings.SCREEN_HEIGHT - settings.GROUND_HEIGHT
        offset = int(self.ground_offset)
        screen.blit(self.ground_surface, (-offset, ground_y))
        screen.blit(self.ground_surface, (settings.SCREEN_WIDTH - offset, ground_y))
    def _draw_cloud(self, screen, x, y, scale):
        """Draw a simple three-lobe cloud."""
        r = int(18 * scale)
        pygame.draw.circle(screen, settings.CLOUD_COLOR, (int(x), int(y)), r)
        pygame.draw.circle(screen, settings.CLOUD_COLOR, (int(x + r * 0.9), int(y + 4)), int(r * 0.75))
        pygame.draw.circle(screen, settings.CLOUD_COLOR, (int(x - r * 0.9), int(y + 5)), int(r * 0.65))