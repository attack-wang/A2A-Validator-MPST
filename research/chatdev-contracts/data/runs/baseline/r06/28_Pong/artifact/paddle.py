'''
paddle.py
Defines the Paddle class: a vertical paddle controlled by a player.
'''
import pygame
from constants import (SCREEN_HEIGHT, PADDLE_SPEED, PADDLE_WIDTH, PADDLE_HEIGHT)
class Paddle:
    """A vertical paddle that a player moves up and down."""
    def __init__(self, x, up_key, down_key, color):
        self.x = x
        self.y = (SCREEN_HEIGHT - PADDLE_HEIGHT) // 2
        self.width = PADDLE_WIDTH
        self.height = PADDLE_HEIGHT
        self.speed = PADDLE_SPEED
        self.up_key = up_key
        self.down_key = down_key
        self.color = color
    def rect(self):
        """Return the paddle's bounding rectangle."""
        return pygame.Rect(int(self.x), int(self.y), self.width, self.height)
    def center_y(self):
        """Return the vertical center of the paddle."""
        return self.y + self.height / 2
    def update(self, keys):
        """Move the paddle according to held keys and clamp to the screen."""
        if keys[self.up_key]:
            self.y -= self.speed
        if keys[self.down_key]:
            self.y += self.speed
        # Clamp within play field
        if self.y < 0:
            self.y = 0
        if self.y + self.height > SCREEN_HEIGHT:
            self.y = SCREEN_HEIGHT - self.height
    def reset(self):
        """Return the paddle to the vertical center of the screen."""
        self.y = (SCREEN_HEIGHT - PADDLE_HEIGHT) // 2
    def draw(self, surface):
        """Render the paddle as a rounded rectangle."""
        pygame.draw.rect(surface, self.color, self.rect(), border_radius=4)