'''Bullet: a projectile fired either by the player's ship or by an alien.'''
import pygame
class Bullet:
    '''A simple rectangular projectile moving straight up or down.'''
    def __init__(self, settings, x, y, direction, color, speed):
        self.settings = settings
        self.direction = direction   # -1 = upward (player), 1 = downward (alien)
        self.color = color
        self.speed = speed
        self.rect = pygame.Rect(0, 0, settings.bullet_width, settings.bullet_height)
        self.rect.center = (int(x), int(y))
    def update(self):
        '''Move the bullet one step along its direction.'''
        self.rect.y += int(self.direction * self.speed)
    def is_off_screen(self):
        '''Return True once the bullet has left the visible play area.'''
        return self.rect.bottom < 0 or self.rect.top > self.settings.screen_height
    def draw(self, screen):
        '''Render the bullet on screen.'''
        pygame.draw.rect(screen, self.color, self.rect)