'''
Paddle class for the Pong game.
Represents one player's vertical paddle: keyboard-driven up/down
movement, clamping to the playfield and rendering.
'''
import pygame
import settings
class Paddle:
    """A vertical paddle moved by two keyboard keys (up/down)."""
    def __init__(self, x, up_key, down_key, color):
        """
        Place the paddle at horizontal position `x`, vertically centered.
        `up_key`/`down_key` are pygame key constants held to move the
        paddle; `color` is the RGB tuple used when drawing.
        """
        self.up_key = up_key
        self.down_key = down_key
        self.color = color
        self.rect = pygame.Rect(
            x,
            (settings.WINDOW_HEIGHT - settings.PADDLE_HEIGHT) // 2,
            settings.PADDLE_WIDTH,
            settings.PADDLE_HEIGHT,
        )
    def update(self, keys):
        """Move the paddle according to currently held keys, clamped to the window."""
        movement = 0
        if keys[self.up_key]:
            movement -= settings.PADDLE_SPEED
        if keys[self.down_key]:
            movement += settings.PADDLE_SPEED
        self.rect.y += movement
        if self.rect.top < 0:
            self.rect.top = 0
        elif self.rect.bottom > settings.WINDOW_HEIGHT:
            self.rect.bottom = settings.WINDOW_HEIGHT
    def draw(self, screen):
        """Render the paddle."""
        pygame.draw.rect(screen, self.color, self.rect)