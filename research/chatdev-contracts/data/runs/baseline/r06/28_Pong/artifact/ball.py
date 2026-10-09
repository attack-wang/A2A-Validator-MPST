'''
ball.py
Defines the Ball class: the ball's motion, wall bounces, paddle collisions,
and point detection.
'''
import math
import random
import pygame
from constants import (
    SCREEN_WIDTH, SCREEN_HEIGHT, BALL_SIZE,
    BALL_INITIAL_SPEED_X, BALL_INITIAL_SPEED_Y_RANGE,
    BALL_SPEED_INCREMENT, BALL_MAX_SPEED, BALL_MAX_BOUNCE_ANGLE,
    WHITE,
)
class Ball:
    """The game ball: moves, bounces off walls and paddles, detects misses."""
    def __init__(self):
        self.size = BALL_SIZE
        self.reset(direction=random.choice([-1, 1]))
    def reset(self, direction):
        """Place the ball at the center and give it a fresh velocity.
        direction: 1 -> serve toward the right, -1 -> serve toward the left.
        """
        self.x = SCREEN_WIDTH / 2 - self.size / 2
        self.y = SCREEN_HEIGHT / 2 - self.size / 2
        speed_y = random.uniform(*BALL_INITIAL_SPEED_Y_RANGE)
        # avoid nearly vertical serves
        while abs(speed_y) < 1.0:
            speed_y = random.uniform(*BALL_INITIAL_SPEED_Y_RANGE)
        self.vx = direction * BALL_INITIAL_SPEED_X
        self.vy = speed_y
        self.speed = math.hypot(self.vx, self.vy)
    def rect(self):
        """Return the ball's bounding rectangle."""
        return pygame.Rect(int(self.x), int(self.y), self.size, self.size)
    def update(self, paddles):
        """
        Move the ball one frame.
        Returns:
            None  -> ball still in play
            0     -> ball exited on the RIGHT side (Player 1 scores)
            1     -> ball exited on the LEFT side  (Player 2 scores)
        """
        self.x += self.vx
        self.y += self.vy
        # Bounce off top and bottom edges
        if self.y <= 0:
            self.y = 0
            self.vy = abs(self.vy)
        elif self.y + self.size >= SCREEN_HEIGHT:
            self.y = SCREEN_HEIGHT - self.size
            self.vy = -abs(self.vy)
        # Paddle collisions
        for paddle in paddles:
            if self.rect().colliderect(paddle.rect()):
                self._bounce_off_paddle(paddle)
        # Out of bounds -> point
        if self.x + self.size < 0:
            return 1  # exited left; Player 2 (index 1) scores
        if self.x > SCREEN_WIDTH:
            return 0  # exited right; Player 1 (index 0) scores
        return None
    def _bounce_off_paddle(self, paddle):
        """Reflect the ball off a paddle.
        The bounce angle depends on where the ball hits the paddle
        (hitting near the top/bottom edge produces a steeper angle),
        and the ball's speed increases slightly with every paddle hit.
        """
        prect = paddle.rect()
        brect = self.rect()
        if self.vx < 0:
            # Ball moving left hit the LEFT paddle -> bounce to the right
            self.x = float(prect.right)          # push ball out of the paddle
            direction = 1
        else:
            # Ball moving right hit the RIGHT paddle -> bounce to the left
            self.x = float(prect.left - self.size)
            direction = -1
        # Relative hit position: -1 at paddle top, 0 at center, +1 at bottom
        rel = (brect.centery - prect.centery) / (prect.height / 2)
        rel = max(-1.0, min(1.0, rel))
        angle = rel * BALL_MAX_BOUNCE_ANGLE
        self.speed = min(self.speed + BALL_SPEED_INCREMENT, BALL_MAX_SPEED)
        self.vx = direction * self.speed * math.cos(angle)
        self.vy = self.speed * math.sin(angle)
    def draw(self, surface):
        """Render the ball as a circle."""
        center = (int(self.x + self.size / 2), int(self.y + self.size / 2))
        pygame.draw.circle(surface, WHITE, center, self.size // 2)