'''
paddle.py
Defines the Paddle class: a vertical bar controlled by a player that moves
up and down, stays inside the screen and can collide with the ball.
'''
import pygame
import settings
class Paddle:
    """A vertical paddle controlled with two keys (up / down)."""
    def __init__(self, x, up_key, down_key):
        self.up_key = up_key
        self.down_key = down_key
        self.speed = settings.PADDLE_SPEED
        self.rect = pygame.Rect(
            x,
            settings.SCREEN_HEIGHT // 2 - settings.PADDLE_HEIGHT // 2,
            settings.PADDLE_WIDTH,
            settings.PADDLE_HEIGHT,
        )
    def update(self, keys):
        """Move the paddle according to the currently pressed keys."""
        if keys[self.up_key]:
            self.rect.y -= self.speed
        if keys[self.down_key]:
            self.rect.y += self.speed
        # Keep the paddle fully inside the window.
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > settings.SCREEN_HEIGHT:
            self.rect.bottom = settings.SCREEN_HEIGHT
    def draw(self, screen):
        pygame.draw.rect(screen, settings.FOREGROUND_COLOR, self.rect)