'''
paddle.py
Defines the Paddle class: a vertical paddle controlled by a player
via keyboard input, used to bounce the ball back.
'''
import pygame
import settings
class Paddle:
    """A vertical paddle that a player moves up and down."""
    def __init__(self, x, up_key, down_key, color):
        """Create a paddle centered vertically at horizontal position x."""
        self.width = settings.PADDLE_WIDTH
        self.height = settings.PADDLE_HEIGHT
        self.x = x
        self.y = (settings.SCREEN_HEIGHT - self.height) // 2
        self.speed = settings.PADDLE_SPEED
        self.up_key = up_key
        self.down_key = down_key
        self.color = color
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
    def update(self, keys):
        """Move the paddle according to held keys and clamp within screen."""
        if keys[self.up_key]:
            self.y -= self.speed
        if keys[self.down_key]:
            self.y += self.speed
        # Clamp within top and bottom edges
        if self.y < 0:
            self.y = 0
        if self.y + self.height > settings.SCREEN_HEIGHT:
            self.y = settings.SCREEN_HEIGHT - self.height
        self.rect.topleft = (self.x, self.y)
    def draw(self, screen):
        """Render the paddle on the screen."""
        pygame.draw.rect(screen, self.color, self.rect)
    def center_y(self):
        """Return the vertical center of the paddle (for bounce angles)."""
        return self.y + self.height / 2