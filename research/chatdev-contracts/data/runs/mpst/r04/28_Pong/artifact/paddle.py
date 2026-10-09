'''
paddle.py
Defines the Paddle class representing a player-controlled vertical paddle.
'''
import pygame
import settings
class Paddle:
    '''A vertical paddle controlled by a player via two keyboard keys.'''
    def __init__(self, x, up_key, down_key, color):
        self.width = settings.PADDLE_WIDTH
        self.height = settings.PADDLE_HEIGHT
        self.x = x
        self.y = (settings.SCREEN_HEIGHT - self.height) // 2
        self.speed = settings.PADDLE_SPEED
        self.up_key = up_key
        self.down_key = down_key
        self.color = color
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
    def update(self):
        '''Move the paddle according to held keys and clamp to screen.'''
        keys = pygame.key.get_pressed()
        dy = 0
        if keys[self.up_key]:
            dy -= self.speed
        if keys[self.down_key]:
            dy += self.speed
        self.y += dy
        # Clamp within playfield
        if self.y < 0:
            self.y = 0
        if self.y > settings.SCREEN_HEIGHT - self.height:
            self.y = settings.SCREEN_HEIGHT - self.height
        self.rect.topleft = (self.x, self.y)
    def reset(self):
        '''Return the paddle to the vertical center of the screen.'''
        self.y = (settings.SCREEN_HEIGHT - self.height) // 2
        self.rect.topleft = (self.x, self.y)
    def draw(self, screen):
        '''Render the paddle.'''
        pygame.draw.rect(screen, self.color, self.rect)
    def center_y(self):
        '''Return the vertical center coordinate of the paddle.'''
        return self.y + self.height / 2