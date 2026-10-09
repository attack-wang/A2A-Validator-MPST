'''
Rendering module: draws background, ground, pipes, bird, HUD and overlay screens.
'''
import math
import random
import pygame
import settings
class Renderer:
    '''Draws every visual element of the game onto the main surface.'''
    STRIPE_WIDTH = 24
    def __init__(self, surface):
        self.surface = surface
        self.sky = self._make_sky()
        self.big_font = pygame.font.SysFont("arial", 52, bold=True)
        self.medium_font = pygame.font.SysFont("arial", 30, bold=True)
        self.small_font = pygame.font.SysFont("arial", 20)
        self.ground_offset = 0.0
        self.time = 0
        self.clouds = [
            {"x": random.uniform(0, settings.SCREEN_WIDTH), "y": random.uniform(40, 220),
             "speed": random.uniform(0.2, 0.6), "scale": random.uniform(0.7, 1.4)}
            for _ in range(5)
        ]
    def _make_sky(self):
        sky = pygame.Surface((settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT))
        top = settings.SKY_TOP
        bottom = settings.SKY_BOTTOM
        for y in range(settings.SCREEN_HEIGHT):
            t = y / settings.SCREEN_HEIGHT
            color = (int(top[0] + (bottom[0] - top[0]) * t),
                     int(top[1] + (bottom[1] - top[1]) * t),
                     int(top[2] + (bottom[2] - top[2]) * t))
            pygame.draw.line(sky, color, (0, y), (settings.SCREEN_WIDTH, y))
        return sky
    def update_background(self, scroll_speed):
        self.time += 1
        self.ground_offset = (self.ground_offset + scroll_speed) % self.STRIPE_WIDTH
        for cloud in self.clouds:
            cloud["x"] -= cloud["speed"]
            if cloud["x"] < -120:
                cloud["x"] = settings.SCREEN_WIDTH + random.uniform(0, 200)
                cloud["y"] = random.uniform(40, 220)
    def draw(self, game):
        self.surface.blit(self.sky, (0, 0))
        self._draw_clouds()
        for pipe in game.pipe_manager.pipes:
            pipe.draw(self.surface)
        game.bird.draw(self.surface)
        self._draw_ground()
        if game.state == "menu":
            self._draw_menu(game)
        elif game.state == "playing":
            self._draw_score(game.score)
        elif game.state == "game_over":
            self._draw_score(game.score)
            self._draw_game_over(game)
        if game.flash_timer > 0:
            flash = pygame.Surface((settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT), pygame.SRCALPHA)
            flash.fill((255, 255, 255, int(255 * game.flash_timer / 8)))
            self.surface.blit(flash, (0, 0))
    def _draw_clouds(self):
        '''Draw drifting semi-transparent clouds.'''
        for cloud in self.clouds:
            s = cloud["scale"]
            x, y = int(cloud["x"]), int(cloud["y"])
            r = int(20 * s)
            color = (255, 255, 255, 180)
            cloud_surf = pygame.Surface((r * 4, r * 2 + 4), pygame.SRCALPHA)
            pygame.draw.circle(cloud_surf, color, (r, r + 4), r)
            pygame.draw.circle(cloud_surf, color, (r * 2, r), int(r * 1.25))
            pygame.draw.circle(cloud_surf, color, (r * 3, r + 4), r)
            pygame.draw.rect(cloud_surf, color, (r, r, r * 2, r + 4))
            self.surface.blit(cloud_surf, (x - r, y - r))
    def _draw_ground(self):
        '''Draw scrolling grass edge and dirt ground.'''
        ground_y = settings.SCREEN_HEIGHT - settings.GROUND_HEIGHT
        pygame.draw.rect(self.surface, settings.GRASS_COLOR, (0, ground_y, settings.SCREEN_WIDTH, 12))
        pygame.draw.rect(self.surface, settings.GROUND_COLOR,
                         (0, ground_y + 12, settings.SCREEN_WIDTH, settings.GROUND_HEIGHT - 12))
        # scrolling diagonal stripes on the grass edge
        for x in range(-self.STRIPE_WIDTH, settings.SCREEN_WIDTH + self.STRIPE_WIDTH, self.STRIPE_WIDTH * 2):
            x0 = x - self.ground_offset
            pygame.draw.polygon(self.surface, settings.GRASS_DARK, [
                (x0, ground_y + 12),
                (x0 + self.STRIPE_WIDTH, ground_y + 12),
                (x0 + self.STRIPE_WIDTH * 2, ground_y),
                (x0 + self.STRIPE_WIDTH, ground_y),
            ])
        # subtle dirt speckles
        ...