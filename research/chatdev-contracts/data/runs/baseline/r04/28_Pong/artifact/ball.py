'''
ball.py
Defines the Ball entity: position, velocity, edge bouncing, serve/reset logic.
'''
import math
import random
import pygame
from settings import (
    BALL_RADIUS,
    BALL_INITIAL_SPEED,
    BALL_MAX_SPEED,
    BALL_SPEEDUP_PER_HIT,
    BALL_MAX_BOUNCE_ANGLE,
    BALL_SERVE_MAX_ANGLE,
    WINDOW_WIDTH,
    WINDOW_HEIGHT,
    COLOR_BALL,
)
class Ball:
    """The ball: bounces off top/bottom walls and is served from center."""
    def __init__(self):
        self.radius = BALL_RADIUS
        self.max_speed = BALL_MAX_SPEED
        self.speedup = BALL_SPEEDUP_PER_HIT
        self.reset(serve_direction=random.choice((-1, 1)))
    # -- position helpers ---------------------------------------------------
    @property
    def rect(self):
        return pygame.Rect(
            int(self.x - self.radius),
            int(self.y - self.radius),
            self.radius * 2,
            self.radius * 2,
        )
    @property
    def left(self):
        return self.x - self.radius
    @property
    def right(self):
        return self.x + self.radius
    # -- lifecycle ----------------------------------------------------------
    def reset(self, serve_direction):
        """Center the ball and aim a fresh serve toward `serve_direction`."""
        self.x = WINDOW_WIDTH / 2.0
        self.y = WINDOW_HEIGHT / 2.0
        self.speed = BALL_INITIAL_SPEED
        self.served = False
        angle = math.radians(random.uniform(-BALL_SERVE_MAX_ANGLE, BALL_SERVE_MAX_ANGLE))
        self.vx = serve_direction * self.speed * math.cos(angle)
        self.vy = self.speed * math.sin(angle)
    def serve(self):
        """Release the ball from its centered waiting position."""
        self.served = True
    # -- simulation ---------------------------------------------------------
    def update(self, dt):
        """Advance the ball; bounce off the top and bottom edges."""
        if not self.served:
            return
        self.x += self.vx * dt
        self.y += self.vy * dt
        if self.y - self.radius <= 0.0 and self.vy < 0.0:
            self.y = self.radius
            self.vy = -self.vy
        elif self.y + self.radius >= WINDOW_HEIGHT and self.vy > 0.0:
            self.y = WINDOW_HEIGHT - self.radius
            self.vy = -self.vy
    def bounce_off_paddle(self, paddle, horizontal_direction):
        """Reflect off `paddle`, angle from hit offset, with a speed boost."""
        half_height = paddle.height / 2.0
        offset = (self.y - paddle.center_y) / half_height
        offset = max(-1.0, min(1.0, offset))
        angle = math.radians(offset * BALL_MAX_BOUNCE_ANGLE)
        self.speed = min(self.speed * self.speedup, self.max_speed)
        self.vx = horizontal_direction * self.speed * math.cos(angle)
        self.vy = self.speed * math.sin(angle)
    # -- rendering ----------------------------------------------------------
    def draw(self, surface):
        pygame.draw.circle(
            surface, COLOR_BALL, (int(self.x), int(self.y)), self.radius
        )