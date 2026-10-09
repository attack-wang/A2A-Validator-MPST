'''
paddle.py
Defines the Paddle entity controlled by the players.
A paddle is a vertical rectangle that slides up and down along its side
of the field in response to keyboard input, always clamped inside the
window bounds.
'''
import pygame
from settings import (
    WINDOW_HEIGHT,
    PADDLE_WIDTH,
    PADDLE_HEIGHT,
    PADDLE_SPEED,
)
class Paddle:
    """Vertical player-controlled paddle on one side of the field."""
    def __init__(self, x, color, up_key, down_key):
        """Place the paddle vertically centered at horizontal position `x`."""
        self.rect = pygame.Rect(x, (WINDOW_HEIGHT - PADDLE_HEIGHT) // 2,
                               PADDLE_WIDTH, PADDLE_HEIGHT)
        self.color = color
        self.up_key = up_key
        self.down_key = down_key
        self.speed = PADDLE_SPEED
    def handle_input(self, keys):
        """Move the paddle according to the currently pressed keys."""
        if keys[self.up_key]:
            self.rect.y -= self.speed
        if keys[self.down_key]:
            self.rect.y += self.speed
        self.clamp_to_screen()
    def clamp_to_screen(self):
        """Keep the paddle fully inside the vertical window bounds."""
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > WINDOW_HEIGHT:
            self.rect.bottom = WINDOW_HEIGHT
    def draw(self, surface):
        """Render the paddle onto the given surface."""
        pygame.draw.rect(surface, self.color, self.rect, border_radius=4)