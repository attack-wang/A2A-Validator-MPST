'''bullet.py — projectiles fired by the ship and by the aliens.'''
import pygame
class Bullet(pygame.sprite.Sprite):
    '''A simple rectangular projectile moving straight up or down.'''
    def __init__(self, game, center_x, top_y, direction, is_alien=False):
        '''Create a bullet. direction: -1 = upward (player), +1 = downward (alien).'''
        super().__init__()
        self.settings = game.settings
        if is_alien:
            width = self.settings.alien_bullet_width
            height = self.settings.alien_bullet_height
            color = self.settings.alien_bullet_color
            speed = self.settings.alien_bullet_speed
        else:
            width = self.settings.bullet_width
            height = self.settings.bullet_height
            color = self.settings.bullet_color
            speed = self.settings.bullet_speed
        self.image = pygame.Surface((width, height))
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.midtop = (center_x, top_y)
        self.y = float(self.rect.y)
        self.speed = speed * direction
    def update(self):
        '''Move the bullet; direction was set at creation time.'''
        self.y += self.speed
        self.rect.y = self.y
    def draw(self, screen):
        '''Draw the bullet on the screen.'''
        screen.blit(self.image, self.rect)