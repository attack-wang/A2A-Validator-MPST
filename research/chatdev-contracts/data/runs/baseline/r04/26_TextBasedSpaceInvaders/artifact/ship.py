'''Player ship: horizontal movement and firing.'''
import pygame
import settings
from bullet import Bullet
class Ship:
    def __init__(self):
        self.rect = pygame.Rect(0, 0, settings.SHIP_WIDTH, settings.SHIP_HEIGHT)
        self.x = 0.0
        self.reset()
        self.cooldown_timer = 0.0
    def reset(self):
        self.x = (settings.SCREEN_WIDTH - settings.SHIP_WIDTH) / 2.0
        self.rect.midbottom = (settings.SCREEN_WIDTH // 2, settings.SCREEN_HEIGHT - 40)
        self.cooldown_timer = 0.0
    def update(self, dt, keys):
        direction = 0
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            direction -= 1
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            direction += 1
        self.x += direction * settings.SHIP_SPEED * dt
        self.x = max(0.0, min(self.x, settings.SCREEN_WIDTH - settings.SHIP_WIDTH))
        self.rect.x = int(round(self.x))
        if self.cooldown_timer > 0:
            self.cooldown_timer = max(0.0, self.cooldown_timer - dt)
    def fire(self):
        if self.cooldown_timer > 0:
            return None
        self.cooldown_timer = settings.SHIP_COOLDOWN
        return Bullet(self.rect.centerx, self.rect.top, -settings.BULLET_SPEED,
                      settings.COLOR_BULLET, settings.BULLET_WIDTH, settings.BULLET_HEIGHT)
    def draw(self, screen):
        # hull
        pygame.draw.polygon(screen, settings.COLOR_SHIP, [
            (self.rect.centerx, self.rect.top),
            (self.rect.right, self.rect.bottom),
            (self.rect.left, self.rect.bottom)
        ])
        # cannon
        pygame.draw.rect(screen, settings.COLOR_SHIP,
                         (self.rect.centerx - 2, self.rect.top - 8, 4, 8))