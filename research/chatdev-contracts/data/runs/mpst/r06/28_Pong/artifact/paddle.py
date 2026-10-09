'''
paddle.py
Defines the Paddle entity: a vertical bar controlled by a player.
Handles keyboard-driven up/down movement and keeps the paddle
inside the playfield boundaries.
'''
import pygame
import settings
class Paddle:
    """Vertical paddle controlled by one player via two keyboard keys."""
    def __init__(self, x, up_key, down_key):
        self.x = x
        self.y = (settings.HEIGHT - settings.PADDLE_HEIGHT) // 2
        self.width = settings.PADDLE_WIDTH
        self.height = settings.PADDLE_HEIGHT
        self.speed = settings.PADDLE_SPEED
        self.up_key = up_key
        self.down_key = down_key
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
    def update(self, keys):
        """Read keyboard state and move the paddle, clamping to the screen."""
        if keys[self.up_key]:
            self.y -= self.speed
        if keys[self.down_key]:
            self.y += self.speed
        # Keep paddle within vertical bounds
        if self.y < 0:
            self.y = 0
        if self.y > settings.HEIGHT - self.height:
            self.y = settings.HEIGHT - self.height
        self.rect.topleft = (self.x, self.y)
    def draw(self, screen):
        pygame.draw.rect(screen, settings.WHITE, self.rect)