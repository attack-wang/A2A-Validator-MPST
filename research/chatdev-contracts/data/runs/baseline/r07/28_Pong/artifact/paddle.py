'''
paddle.py
Defines the Paddle class: a vertical paddle controlled by a player.
Updated to include reset_position (previously lost in a stray file),
which Game._restart_match relies on to re-center paddles.
'''
import pygame
from constants import (PADDLE_WIDTH, PADDLE_HEIGHT, PADDLE_SPEED,
                       WINDOW_HEIGHT, COLOR_FOREGROUND)
class Paddle:
    '''A vertical paddle that a player moves up and down with keyboard keys.'''
    def __init__(self, x, up_key, down_key, color):
        '''Create a paddle centered vertically at horizontal position x.'''
        self.x = x
        self.y = (WINDOW_HEIGHT - PADDLE_HEIGHT) // 2
        self.width = PADDLE_WIDTH
        self.height = PADDLE_HEIGHT
        self.speed = PADDLE_SPEED
        self.up_key = up_key
        self.down_key = down_key
        self.color = color
    def update(self, keys):
        '''Move the paddle according to held keys and clamp within the window.'''
        if keys[self.up_key]:
            self.y -= self.speed
        if keys[self.down_key]:
            self.y += self.speed
        # Clamp so the paddle never leaves the play area
        if self.y < 0:
            self.y = 0
        if self.y > WINDOW_HEIGHT - self.height:
            self.y = WINDOW_HEIGHT - self.height
    def reset_position(self):
        '''Return the paddle to the vertical center of the window.'''
        self.y = (WINDOW_HEIGHT - self.height) // 2
    def get_rect(self):
        '''Return the pygame.Rect used for collision and drawing.'''
        return pygame.Rect(int(self.x), int(self.y), self.width, self.height)
    def draw(self, surface):
        '''Render the paddle onto the given surface.'''
        pygame.draw.rect(surface, self.color, self.get_rect())