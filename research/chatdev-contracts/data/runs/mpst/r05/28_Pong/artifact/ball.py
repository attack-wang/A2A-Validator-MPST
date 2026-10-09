'''
ball.py
Defines the Ball entity and its physics.
The ball keeps its position as floats for smooth sub-pixel motion and
syncs it into an integer rect for collision and drawing. It travels with
a speed magnitude that grows slightly on every paddle hit, bounces off
the top/bottom edges, is deflected vertically depending on where it
strikes a paddle, reports when it leaves the field, and can be reset to
the center for the next serve.
'''
import math
import random
import pygame
from settings import (
    WINDOW_WIDTH,
    WINDOW_HEIGHT,
    BALL_SIZE,
    BALL_INITIAL_SPEED,
    BALL_MAX_SPEED,
    BALL_SPEED_INCREMENT,
    MAX_DEFLECTION_ANGLE,
    SERVE_MAX_ANGLE,
    COLOR_BALL,
)
class Ball:
    """The bouncing ball with serve, movement, deflection and drawing."""
    def __init__(self):
        """Create the ball centered and frozen, ready for the first serve."""
        self.rect = pygame.Rect(0, 0, BALL_SIZE, BALL_SIZE)
        self.x = float(WINDOW_WIDTH // 2)
        self.y = float(WINDOW_HEIGHT // 2)
        self.speed = BALL_INITIAL_SPEED
        self.vx = 0.0
        self.vy = 0.0
        self.frozen = True          # True while waiting to be served
        self.serve_direction = 1    # +1 serves right, -1 serves left
        self.reset(random.choice((-1, 1)))
    def _sync_rect(self):
        """Copy the float position into the integer rect used for collisions."""
        self.rect.centerx = int(round(self.x))
        self.rect.centery = int(round(self.y))
    def reset(self, serve_direction):
        """Center the ball, restore base speed and freeze it before a serve."""
        self.x = float(WINDOW_WIDTH // 2)
        self.y = float(WINDOW_HEIGHT // 2)
        self._sync_rect()
        self.speed = BALL_INITIAL_SPEED
        self.vx = 0.0
        self.vy = 0.0
        self.frozen = True
        self.serve_direction = serve_direction
    def launch(self):
        """Unfreeze the ball and send it toward `serve_direction` at a random angle."""
        angle = math.radians(random.uniform(-SERVE_MAX_ANGLE, SERVE_MAX_ANGLE))
        self.vx = self.serve_direction * self.speed * math.cos(angle)
        self.vy = self.speed * math.sin(angle)
        self.frozen = False
    def update(self):
        """Advance the ball one frame and bounce off the top/bottom edges."""
        if self.frozen:
            return
        self.x += self.vx
        self.y += self.vy
        half = BALL_SIZE / 2
        if self.y - half <= 0:
            self.y = half
            self.vy = abs(self.vy)
        elif self.y + half >= WINDOW_HEIGHT:
            self.y = WINDOW_HEIGHT - half
            self.vy = -abs(self.vy)
        self._sync_rect()
    def bounce_off_paddle(self, paddle):
        """Reflect the ball off `paddle`, deflecting by the hit position and speeding up."""
        # Speed up (capped) to keep rallies escalating.
        self.speed = min(self.speed + BALL_SPEED_INCREMENT, BALL_MAX_SPEED)
        # New horizontal direction points away from the struck paddle.
        direction = 1 if paddle.rect.centerx < self.x else -1
        # Vertical deflection grows with distance from the paddle's center.
        max_offset = paddle.rect.height / 2
        offset = (self.y - paddle.rect.centery) / max_offset
        offset = max(-1.0, min(1.0, offset))
        angle = math.radians(MAX_DEFLECTION_ANGLE) * offset
        self.vx = direction * self.speed * math.cos(angle)
        self.vy = self.speed * math.sin(angle)
        # Push the ball just outside the paddle face so it cannot stick.
        if direction == 1:
            self.x = paddle.rect.right + BALL_SIZE / 2
        else:
            self.x = paddle.rect.left - BALL_SIZE / 2
        self._sync_rect()
    def is_out_left(self):
        """True when the ball fully crossed the left edge (left player missed)."""
        return self.rect.right < 0
    def is_out_right(self):
        """True when the ball fully crossed the right edge (right player missed)."""
        return self.rect.left > WINDOW_WIDTH
    def draw(self, surface):
        """Render the ball as a rounded square onto the given surface."""
        pygame.draw.rect(surface, COLOR_BALL, self.rect, border_radius=BALL_SIZE // 2)