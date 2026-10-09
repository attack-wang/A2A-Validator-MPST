'''
paddle.py
Defines the Paddle entity used by both players.
A paddle is a vertical rectangle that can be moved up and down.
Movement is clamped so the paddle never leaves the playfield.
'''
import pygame
import settings
class Paddle:
    '''Vertical paddle controlled by a player (moves up / down only).'''
    def __init__(self, side):
        '''
        Create a paddle.
        side: 'left' or 'right' -- decides the starting x position
              and the colour used for drawing.
        '''
        self.side = side
        self.speed = settings.PADDLE_SPEED
        x = settings.PADDLE_MARGIN if side == 'left' else \
            settings.SCREEN_WIDTH - settings.PADDLE_MARGIN - settings.PADDLE_WIDTH
        y = (settings.SCREEN_HEIGHT - settings.PADDLE_HEIGHT) // 2
        self.rect = pygame.Rect(x, y, settings.PADDLE_WIDTH, settings.PADDLE_HEIGHT)
        self.color = settings.COLOR_PADDLE_LEFT if side == 'left' else settings.COLOR_PADDLE_RIGHT
    def move_up(self):
        '''Move the paddle towards the top of the screen.'''
        self.rect.y -= self.speed
        self._clamp()
    def move_down(self):
        '''Move the paddle towards the bottom of the screen.'''
        self.rect.y += self.speed
        self._clamp()
    def _clamp(self):
        '''Keep the paddle fully inside the playfield.'''
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > settings.SCREEN_HEIGHT:
            self.rect.bottom = settings.SCREEN_HEIGHT
    def draw(self, surface):
        '''Render the paddle on the given surface.'''
        pygame.draw.rect(surface, self.color, self.rect, border_radius=6)