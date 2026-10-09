'''Player ship sprite for the Space Invaders game.'''
import pygame
from settings import (SCREEN_WIDTH, SCREEN_HEIGHT, SHIP_WIDTH, SHIP_HEIGHT,
                      SHIP_SPEED, SHIP_COOLDOWN, INVINCIBLE_FRAMES,
                      GREEN, CYAN)
from bullets import Bullet
class Ship(pygame.sprite.Sprite):
    '''The player-controlled ship: moves horizontally, fires bullets,
    and blinks while invincible after respawn.'''
    def __init__(self, game):
        super().__init__()
        self.game = game
        self.image = self._make_image()
        self.rect = self.image.get_rect(
            midbottom=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 20))
        self.cooldown = 0
        self.invincible = 0
    def _make_image(self):
        w, h = SHIP_WIDTH, SHIP_HEIGHT
        surf = pygame.Surface((w, h), pygame.SRCALPHA)
        points = [
            (w * 0.5, 0),
            (w, h * 0.55),
            (w * 0.75, h * 0.55),
            (w * 0.75, h),
            (w * 0.25, h),
            (w * 0.25, h * 0.55),
            (0, h * 0.55),
        ]
        pygame.draw.polygon(surf, GREEN, points)
        pygame.draw.circle(surf, CYAN, (w // 2, int(h * 0.35)), 4)
        return surf
    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.rect.x -= SHIP_SPEED
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.rect.x += SHIP_SPEED
        # Clamp horizontally within the screen
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
        if self.cooldown > 0:
            self.cooldown -= 1
        if self.invincible > 0:
            self.invincible -= 1
    def shoot(self):
        if self.cooldown <= 0:
            self.game.player_bullets.add(
                Bullet(self.rect.centerx, self.rect.top))
            self.cooldown = SHIP_COOLDOWN
    def respawn(self):
        self.rect.midbottom = (SCREEN_WIDTH // 2, SCREEN_HEIGHT - 20)
        self.invincible = INVINCIBLE_FRAMES
    def draw(self, surface):
        # Blink by skipping draws on alternating frames while invincible
        if self.invincible > 0 and (self.invincible // 6) % 2 == 0:
            return
        surface.blit(self.image, self.rect)