'''Ship: the player-controlled vessel at the bottom of the screen.'''
import pygame
from bullet import Bullet
class Ship:
    '''Player ship with horizontal movement and a cooldown-limited cannon.'''
    def __init__(self, settings):
        self.settings = settings
        self.rect = pygame.Rect(0, 0, settings.ship_width, settings.ship_height)
        self.moving_right = False
        self.moving_left = False
        self.last_shot_ms = 0
        self.reset_position()
    def reset_position(self):
        '''Center the ship at the bottom of the screen.'''
        self.rect.midbottom = (self.settings.screen_width // 2,
                               self.settings.screen_height - 10)
    def update(self):
        '''Apply horizontal movement, clamped to the screen edges.'''
        if self.moving_right and self.rect.right < self.settings.screen_width:
            self.rect.x += self.settings.ship_speed
        if self.moving_left and self.rect.left > 0:
            self.rect.x -= self.settings.ship_speed
    def can_fire(self, now_ms):
        '''Return True if the fire cooldown has elapsed.'''
        return now_ms - self.last_shot_ms >= self.settings.fire_cooldown_ms
    def fire(self, now_ms):
        '''Create an upward bullet from the ship's cannon; record shot time.'''
        self.last_shot_ms = now_ms
        return Bullet(self.settings, self.rect.centerx, self.rect.top,
                      -1, self.settings.player_bullet_color,
                      self.settings.player_bullet_speed)
    def draw(self, screen):
        '''Render the ship with a simple cockpit detail.'''
        pygame.draw.rect(screen, self.settings.ship_color, self.rect, border_radius=6)
        pygame.draw.rect(screen, (255, 255, 255),
                         (self.rect.centerx - 5, self.rect.top + 5, 10, 8))