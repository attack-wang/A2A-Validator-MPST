'''
Paddle module: defines the Paddle class used by both players.
A paddle is a vertical rectangle that a player moves up and down with two
keyboard keys. Movement is clamped so the paddle never leaves the screen.
'''
import pygame
import settings
class Paddle:
    '''A vertical paddle controlled by one player via two keyboard keys.'''
    def __init__(self, x, up_key, down_key, color):
        '''Place the paddle at horizontal position `x`, vertically centered.
        Args:
            x: left pixel coordinate of the paddle.
            up_key: pygame key constant that moves the paddle up.
            down_key: pygame key constant that moves the paddle down.
            color: (R, G, B) tuple used to draw the paddle.
        '''
        self.width = settings.PADDLE_WIDTH
        self.height = settings.PADDLE_HEIGHT
        self.speed = settings.PADDLE_SPEED
        self.up_key = up_key
        self.down_key = down_key
        self.color = color
        # Start vertically centered on the player's side
        self.x = x
        self.y = (settings.SCREEN_HEIGHT - self.height) // 2
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
    def update(self, keys):
        '''Move the paddle according to currently pressed keys.
        Args:
            keys: sequence returned by pygame.key.get_pressed().
        '''
        if keys[self.up_key]:
            self.y -= self.speed
        if keys[self.down_key]:
            self.y += self.speed
        # Clamp so the paddle stays fully inside the window
        if self.y < 0:
            self.y = 0
        elif self.y > settings.SCREEN_HEIGHT - self.height:
            self.y = settings.SCREEN_HEIGHT - self.height
        self.rect.topleft = (self.x, self.y)
    def draw(self, screen):
        '''Render the paddle onto the given surface.'''
        pygame.draw.rect(screen, self.color, self.rect)