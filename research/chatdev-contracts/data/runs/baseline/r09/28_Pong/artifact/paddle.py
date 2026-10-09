'''
paddle.py
Defines the Paddle class: a vertical paddle controlled by a player.
Movement is clamped to the playfield so it can never leave the screen.
'''
import pygame
import settings
class Paddle:
    '''A vertical paddle moved up/down by a player's keys.'''
    def __init__(self, x, y, color):
        '''Create a paddle at (x, y) with the given color.'''
        self.x = float(x)
        self.y = float(y)
        self.width = settings.PADDLE_WIDTH
        self.height = settings.PADDLE_HEIGHT
        self.color = color
        self.speed = settings.PADDLE_SPEED
        self.rect = pygame.Rect(int(self.x), int(self.y), self.width, self.height)
    def move_up(self):
        '''Move the paddle up, staying inside the top edge.'''
        self.y -= self.speed
        self._clamp()
        return self
    def move_down(self):
        '''Move the paddle down, staying inside the bottom edge.'''
        self.y += self.speed
        self._clamp()
        return self
    def _clamp(self):
        '''Keep the paddle fully inside the playfield.'''
        if self.y < 0:
            self.y = 0
        elif self.y + self.height > settings.SCREEN_HEIGHT:
            self.y = settings.SCREEN_HEIGHT - self.height
        self.rect.topleft = (int(self.x), int(self.y))
    def update(self, keys, up_key, down_key):
        '''Read the keyboard state and move the paddle accordingly.'''
        if keys[up_key]:
            self.move_up()
        if keys[down_key]:
            self.move_down()
    def center_vertically(self):
        '''Return the paddle to the vertical center of the playfield.'''
        self.y = (settings.SCREEN_HEIGHT - self.height) / 2
        self._clamp()
    def draw(self, surface):
        '''Render the paddle onto the given surface.'''
        pygame.draw.rect(surface, self.color, self.rect)