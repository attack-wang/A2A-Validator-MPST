'''
paddle.py
Defines the Paddle class: a vertical paddle controlled by a player
using two keys (up/down), constrained to stay inside the window.
'''
import pygame
import constants as c
class Paddle:
    '''A vertical paddle controlled by keyboard keys.'''
    def __init__(self, side, up_key, down_key):
        '''
        Initialize the paddle on the given side ("left" or "right")
        with the specified control keys.
        '''
        self.side = side
        self.up_key = up_key
        self.down_key = down_key
        if side == "left":
            self.x = c.PADDLE_OFFSET
            self.color = c.COLOR_PADDLE_LEFT
        else:
            self.x = c.WINDOW_WIDTH - c.PADDLE_OFFSET - c.PADDLE_WIDTH
            self.color = c.COLOR_PADDLE_RIGHT
        self.y = (c.WINDOW_HEIGHT - c.PADDLE_HEIGHT) // 2
        self.speed = c.PADDLE_SPEED
        self.rect = pygame.Rect(self.x, self.y, c.PADDLE_WIDTH, c.PADDLE_HEIGHT)
    def update(self, keys):
        '''Move the paddle up/down according to pressed keys, clamped to window.'''
        if keys[self.up_key]:
            self.y -= self.speed
        if keys[self.down_key]:
            self.y += self.speed
        self.clamp_position()
        self.rect.topleft = (self.x, self.y)
    def clamp_position(self):
        '''Keep the paddle within the top and bottom window edges.'''
        if self.y < 0:
            self.y = 0
        if self.y > c.WINDOW_HEIGHT - c.PADDLE_HEIGHT:
            self.y = c.WINDOW_HEIGHT - c.PADDLE_HEIGHT
    def get_rect(self):
        '''Return the collision rectangle of the paddle.'''
        return self.rect
    def draw(self, surface):
        '''Render the paddle on the given surface.'''
        pygame.draw.rect(surface, self.color, self.rect, border_radius=4)