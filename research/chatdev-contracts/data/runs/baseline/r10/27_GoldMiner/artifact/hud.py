'''
HUD rendering: score bar, timer, goal, messages, floating texts and effects.
'''
import math
import pygame
import settings
class FloatingText:
    """Small text that rises and fades (e.g. '+$150')."""
    def __init__(self, x, y, text, color=settings.WHITE, size=22, life=1.2):
        self.x = x
        self.y = y
        self.text = text
        self.color = color
        self.size = size
        self.life = life
        self.max_life = life
        self.font = pygame.font.SysFont("arial", size, bold=True)
    def update(self, dt):
        self.y -= 30 * dt
        self.life -= dt
    def draw(self, surface):
        alpha = max(0, int(255 * self.life / self.max_life))
        img = self.font.render(self.text, True, self.color)
        img.set_alpha(alpha)
        surface.blit(img, (int(self.x - img.get_width() / 2), int(self.y)))
class Explosion:
    """Expanding ring effect for TNT blasts."""
    def __init__(self, x, y, radius):
        self.x = x
        self.y = y
        self.radius = radius
        self.t = 0.0
        self.duration = 0.5
    def update(self, dt):
        self.t += dt
    @property
    def done(self):
        return self.t >= self.duration
    def draw(self, surface):
        progress = min(self.t / self.duration, 1.0)
        r = int(self.radius * progress)
        if r <= 0:
            return
        width = max(2, int(10 * (1 - progress)))
        color = settings.ORANGE if progress < 0.6 else settings.RED
        pygame.draw.circle(surface, color, (int(self.x), int(self.y)), r, width)
def draw_background(surface):
    """Sky gradient on top, dirt with speckles below."""
    # vertical sky gradient
    sky_h = settings.PLAY_AREA_TOP
    for row in range(sky_h):
        t = row / max(sky_h - 1, 1)
        color = tuple(int(a + (b - a) * t) for a, b in zip(settings.SKY_TOP, settings.SKY_BOTTOM))
        pygame.draw.line(surface, color, (0, row), (settings.SCREEN_WIDTH, row))
    # dirt block
    dirt_rect = pygame.Rect(0, settings.PLAY_AREA_TOP,
                            settings.SCREEN_WIDTH,
                            settings.SCREEN_HEIGHT - settings.PLAY_AREA_TOP)
    pygame.draw.rect(surface, settings.DIRT, dirt_rect)
    pygame.draw.line(surface, settings.DIRT_TOP,
                     (0, settings.PLAY_AREA_TOP),
                     (settings.SCREEN_WIDTH, settings.PLAY_AREA_TOP), 6)
    # deterministic speckles for texture
    import random as _random
    rng = _random.Random(42)
    for _ in range(120):
        x = rng.randint(10, settings.SCREEN_WIDTH - 10)
        y = rng.randint(settings.PLAY_AREA_TOP + 10, settings.SCREEN_HEIGHT - 10)
        pygame.draw.circle(surface, settings.DIRT_DARK, (x, y), rng.randint(2, 5))