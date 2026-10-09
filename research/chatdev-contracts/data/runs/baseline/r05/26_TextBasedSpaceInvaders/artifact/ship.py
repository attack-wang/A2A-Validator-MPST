import pygame
from settings import Settings
from bullet import Bullet
from utils import bitmap_to_surface
SHIP_BITMAP = [
    ".....XX.....",
    ".....XX.....",
    "....XXXX....",
    ".XXXXXXXXXX.",
    "XXXXXXXXXXXX",
    "XXXXXXXXXXXX",
    "XX.XX..XX.XX",
]
class Ship:
    """Player ship: horizontal movement, cooldown-limited firing."""
    def __init__(self):
        self.image = bitmap_to_surface(SHIP_BITMAP, Settings.SHIP_COLOR, Settings.SHIP_SCALE)
        self.rect = self.image.get_rect(midbottom=(Settings.SCREEN_WIDTH // 2, Settings.SCREEN_HEIGHT - 10))
        self.x = float(self.rect.x)
        self.speed = Settings.SHIP_SPEED
        self.cooldown = 0.0
    def update(self, dt, keys):
        self.cooldown = max(0.0, self.cooldown - dt)
        move = 0
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            move -= 1
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            move += 1
        self.x += move * self.speed * dt
        self.x = max(0.0, min(self.x, Settings.SCREEN_WIDTH - self.rect.width))
        self.rect.x = round(self.x)
    def can_shoot(self, active_bullets):
        return self.cooldown <= 0 and active_bullets < Settings.MAX_PLAYER_BULLETS
    def shoot(self):
        self.cooldown = Settings.SHIP_COOLDOWN
        return Bullet(self.rect.centerx, self.rect.top)
    def center(self):
        self.x = (Settings.SCREEN_WIDTH - self.rect.width) / 2.0
        self.rect.x = round(self.x)
    def draw(self, screen):
        screen.blit(self.image, self.rect)