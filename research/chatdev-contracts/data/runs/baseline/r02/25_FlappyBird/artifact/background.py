"""Background scenery: sky gradient, drifting clouds and scrolling ground."""
import random
import pygame
import settings
class Cloud:
    """A simple drifting cloud made of overlapping circles."""
    def __init__(self, x, y, speed, scale):
        self.x = x
        self.y = y
        self.speed = speed
        self.scale = scale
    def update(self, dt):
        """Drift the cloud leftwards and wrap around to the right edge."""
        self.x -= self.speed * dt
        if self.x < -120 * self.scale:
            self.x = settings.SCREEN_WIDTH + random.randint(10, 120)
            self.y = random.randint(40, 200)
    def draw(self, surface):
        """Render the cloud as a group of circles."""
        s = self.scale
        color = settings.CLOUD_COLOR
        for dx, dy, r in ((0, 0, 26), (24, 6, 20), (-24, 8, 18), (8, -12, 18), (-10, -8, 16)):
            pygame.draw.circle(surface, color,
                               (int(self.x + dx * s), int(self.y + dy * s)), int(r * s))
class Background:
    """Sky gradient, clouds and the scrolling ground strip."""
    def __init__(self):
        self.ground_offset = 0.0
        self.clouds = [Cloud(random.randint(0, settings.SCREEN_WIDTH),
                             random.randint(40, 220),
                             random.uniform(12, 30),
                             random.uniform(0.7, 1.4))
                       for _ in range(5)]
        # pre-render the sky gradient once for performance
        self.sky = pygame.Surface((settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT))
        top = settings.SKY_TOP
        bottom = settings.SKY_BOTTOM
        for row in range(settings.SCREEN_HEIGHT):
            t = row / settings.SCREEN_HEIGHT
            color = (int(top[0] + (bottom[0] - top[0]) * t),
                     int(top[1] + (bottom[1] - top[1]) * t),
                     int(top[2] + (bottom[2] - top[2]) * t))
            pygame.draw.line(self.sky, color, (0, row), (settings.SCREEN_WIDTH, row))
    def update(self, dt, speed):
        """Scroll ground and drift clouds."""
        self.ground_offset = (self.ground_offset + speed * dt) % 24
        for cloud in self.clouds:
            cloud.update(dt)
    def get_ground_top(self):
        """Y coordinate where the ground strip begins."""
        return settings.SCREEN_HEIGHT - settings.GROUND_HEIGHT
    def collide_ground(self, bird_rect):
        """Return True when the bird rect touches the ground strip."""
        return bird_rect.bottom >= self.get_ground_top()
    def draw(self, surface):
        """Draw sky, clouds and ground."""
        surface.blit(self.sky, (0, 0))
        for cloud in self.clouds:
            cloud.draw(surface)
        ground_top = self.get_ground_top()
        # grass strip
        pygame.draw.rect(surface, settings.GRASS_COLOR,
                         (0, ground_top, settings.SCREEN_WIDTH, 14))
        pygame.draw.rect(surface, settings.GRASS_DARK,
                         (0, ground_top + 14, settings.SCREEN_WIDTH, 4))
        # dirt with repeating pattern
        pygame.draw.rect(surface, settings.GROUND_COLOR,
                         (0, ground_top + 18, settings.SCREEN_WIDTH, settings.GROUND_HEIGHT - 18))
        # scrolling stripes on the dirt
        x = -int(self.ground_offset)
        while x < settings.SCREEN_WIDTH:
            pygame.draw.rect(surface, settings.GROUND_DARK,
                             (x, ground_top + 18, 12, settings.GROUND_HEIGHT - 18))
            x += 24
        # grass edge line
        pygame.draw.line(surface, settings.GRASS_DARK, (0, ground_top), (settings.SCREEN_WIDTH, ground_top), 2)