'''ship.py: the player-controlled ship.'''
import pygame
from bullet import Bullet
class Ship:
    def __init__(self, game):
        self.game = game
        self.settings = game.settings
        self.screen = game.screen
        s = self.settings
        self.width = s.ship_width
        self.height = s.ship_height
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.midbottom = (s.screen_width // 2, s.screen_height - 20)
        self.x = float(self.rect.x)
        self.color = s.ship_color
        self.cooldown = 0.0
    def update(self, dt):
        keys = pygame.key.get_pressed()
        move = 0
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            move -= 1
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            move += 1
        self.x += move * self.settings.ship_speed * dt
        self.x = max(0.0, min(self.x, self.settings.screen_width - self.width))
        self.rect.x = int(self.x)
        self.cooldown = max(0.0, self.cooldown - dt)
    def fire(self):
        """Return a new Bullet if allowed, else None."""
        s = self.settings
        if self.cooldown <= 0 and len(self.game.bullets) < s.max_active_bullets:
            self.cooldown = s.bullet_cooldown
            return Bullet(s, self.rect.centerx, self.rect.top,
                          s.bullet_speed, s.bullet_color,
                          s.bullet_width, s.bullet_height, -1)
        return None
    def center_ship(self):
        self.rect.midbottom = (self.settings.screen_width // 2, self.settings.screen_height - 20)
        self.x = float(self.rect.x)
        self.cooldown = 0.0
    def draw(self):
        pygame.draw.rect(self.screen, self.color, self.rect, border_radius=6)
        # cannon
        pygame.draw.rect(self.screen, self.color,
                         (self.rect.centerx - 2, self.rect.top - 8, 4, 8))
        # cockpit window
        window = pygame.Rect(self.rect.centerx - 6, self.rect.y + 8, 12, 8)
        pygame.draw.rect(self.screen, (240, 250, 255), window)