'''
paddle.py
Defines the Paddle class: a vertical paddle driven by two keyboard keys,
clamped inside the court, with score tracking and rendering.
'''
import pygame
from constants import SCREEN_HEIGHT, PADDLE_WIDTH, PADDLE_HEIGHT, PADDLE_SPEED
class Paddle:
    """A vertical paddle moved up and down with two keyboard keys."""
    def __init__(self, x, up_key, down_key, color):
        self.x = x
        self.up_key = up_key
        self.down_key = down_key
        self.color = color
        self.score = 0
        self.y = 0
        self.reset()
    def reset(self):
        """Center the paddle vertically (used at game start)."""
        self.y = (SCREEN_HEIGHT - PADDLE_HEIGHT) // 2
    def move(self, keys):
        """Move the paddle according to the currently held keys."""
        if keys[self.up_key]:
            self.y -= PADDLE_SPEED
        if keys[self.down_key]:
            self.y += PADDLE_SPEED
        # Clamp so the paddle never leaves the top/bottom edges.
        if self.y < 0:
            self.y = 0
        elif self.y > SCREEN_HEIGHT - PADDLE_HEIGHT:
            self.y = SCREEN_HEIGHT - PADDLE_HEIGHT
    def get_rect(self):
        """Return the pygame Rect describing the paddle's position/size."""
        return pygame.Rect(self.x, self.y, PADDLE_WIDTH, PADDLE_HEIGHT)
    def draw(self, screen):
        """Render the paddle in its player's color."""
        pygame.draw.rect(screen, self.color, self.get_rect())