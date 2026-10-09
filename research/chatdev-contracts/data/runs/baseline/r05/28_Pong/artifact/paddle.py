'''
paddle.py
Defines the Paddle class: a vertical paddle controlled by one player
through two keyboard keys (up/down). Handles input-driven movement,
clamping to the court boundaries, score storage, and rendering.
'''
import pygame
import settings
class Paddle:
    '''A vertical paddle moved up and down by keyboard input.'''
    def __init__(self, x, up_key, down_key, color):
        '''Create a paddle at horizontal position x, vertically centered.'''
        self.width = settings.PADDLE_WIDTH
        self.height = settings.PADDLE_HEIGHT
        self.x = x
        self.y = (settings.SCREEN_HEIGHT - self.height) // 2
        self.speed = settings.PADDLE_SPEED
        self.up_key = up_key
        self.down_key = down_key
        self.color = color
        self.score = 0
    def get_rect(self):
        '''Return the pygame.Rect used for collision tests and drawing.'''
        return pygame.Rect(int(self.x), int(self.y), self.width, self.height)
    def move(self, keys):
        '''Move the paddle according to currently held keys, then clamp.'''
        if keys[self.up_key]:
            self.y -= self.speed
        if keys[self.down_key]:
            self.y += self.speed
        self.clamp()
    def clamp(self):
        '''Keep the paddle fully inside the top and bottom screen edges.'''
        if self.y < 0:
            self.y = 0
        elif self.y + self.height > settings.SCREEN_HEIGHT:
            self.y = settings.SCREEN_HEIGHT - self.height
    def reset_position(self):
        '''Return the paddle to its initial vertically centered position.'''
        self.y = (settings.SCREEN_HEIGHT - self.height) // 2
    def draw(self, screen):
        '''Render the paddle onto the given screen surface.'''
        pygame.draw.rect(screen, self.color, self.get_rect())