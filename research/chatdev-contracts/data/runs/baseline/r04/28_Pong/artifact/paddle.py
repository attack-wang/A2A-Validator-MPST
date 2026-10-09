'''
paddle.py
Defines the Paddle entity: a vertical bar moved up and down by a player,
clamped to the playfield, and used for bouncing the ball.
'''
import pygame
from settings import (
    PADDLE_WIDTH,
    PADDLE_HEIGHT,
    PADDLE_SPEED,
    PADDLE_MARGIN,
    PADDLE_CORNER_RADIUS,
    WINDOW_WIDTH,
    WINDOW_HEIGHT,
)
class Paddle:
    """A vertical paddle controlled by one player via two keys."""
    def __init__(self, side, up_key, down_key, color):
        if side not in ("left", "right"):
            raise ValueError("side must be 'left' or 'right'")
        self.side = side
        self.up_key = up_key
        self.down_key = down_key
        self.color = color
        self.speed = PADDLE_SPEED
        self.width = PADDLE_WIDTH
        self.height = PADDLE_HEIGHT
        if side == "left":
            self.x = PADDLE_MARGIN
        else:
            self.x = WINDOW_WIDTH - PADDLE_MARGIN - PADDLE_WIDTH
        self.y = (WINDOW_HEIGHT - PADDLE_HEIGHT) / 2.0
    @property
    def rect(self):
        """Collision rectangle (floats truncated to ints by pygame.Rect)."""
        return pygame.Rect(int(self.x), int(self.y), self.width, self.height)
    @property
    def center_y(self):
        return self.y + self.height / 2.0
    def reset_position(self):
        self.y = (WINDOW_HEIGHT - PADDLE_HEIGHT) / 2.0
    def update(self, dt, keys):
        """Move the paddle according to held keys; clamp to playfield."""
        direction = 0.0
        if keys[self.up_key]:
            direction -= 1.0
        if keys[self.down_key]:
            direction += 1.0
        if direction != 0.0:
            self.y += direction * self.speed * dt
            top_limit = 0.0
            bottom_limit = WINDOW_HEIGHT - self.height
            if self.y < top_limit:
                self.y = top_limit
            elif self.y > bottom_limit:
                self.y = bottom_limit
    def draw(self, surface):
        pygame.draw.rect(
            surface, self.color, self.rect, border_radius=PADDLE_CORNER_RADIUS
        )