'''
ball.py
Defines the Ball class: movement, wall bounces, paddle bounces with
angle control and speed-up, off-screen detection, and rendering.
'''
import math
import random
import pygame
from constants import (SCREEN_WIDTH, SCREEN_HEIGHT, BALL_SIZE,
                       BALL_SPEED_X, BALL_SPEED_Y, BALL_SPEEDUP,
                       MAX_BALL_SPEED, MAX_BOUNCE_ANGLE, WHITE)
class Ball:
    """The game ball with position, velocity, and bounce behavior."""
    def __init__(self):
        self.size = BALL_SIZE
        self.reset_position()
        self.speed_x = 0
        self.speed_y = 0
        self.moving = False
    def reset_position(self):
        """Place the ball at the center of the court."""
        self.x = (SCREEN_WIDTH - self.size) // 2
        self.y = (SCREEN_HEIGHT - self.size) // 2
    def serve(self, direction):
        """Reset and launch the ball toward the given side (+1 right, -1 left)."""
        self.reset_position()
        angle = random.uniform(-0.5, 0.5)  # slight random vertical angle
        self.speed_x = BALL_SPEED_X * direction
        self.speed_y = BALL_SPEED_Y * angle * 2
        self.moving = True
    def update(self):
        """Advance the ball by its velocity."""
        if not self.moving:
            return
        self.x += self.speed_x
        self.y += self.speed_y
    def get_rect(self):
        """Return the pygame Rect representing the ball."""
        return pygame.Rect(int(self.x), int(self.y), self.size, self.size)
    def bounce_off_wall(self):
        """Reflect the vertical velocity when hitting top/bottom edges."""
        self.speed_y = -self.speed_y
        # Nudge back inside to avoid sticking on the edge
        rect = self.get_rect()
        if rect.top <= 0:
            self.y = 0
        elif rect.bottom >= SCREEN_HEIGHT:
            self.y = SCREEN_HEIGHT - self.size
    def bounce_off_paddle(self, paddle):
        """Reflect horizontally, add spin based on hit position, and speed up."""
        rect = self.get_rect()
        paddle_rect = paddle.get_rect()
        # Determine horizontal direction after bounce
        direction = 1 if self.speed_x < 0 else -1
        # Relative hit position: -1 (top of paddle) .. +1 (bottom)
        paddle_center = paddle_rect.centery
        hit_offset = (rect.centery - paddle_center) / (paddle_rect.height / 2)
        hit_offset = max(-1.0, min(1.0, hit_offset))
        # Compute new velocity from angle and current speed
        speed = math.hypot(self.speed_x, self.speed_y)
        speed = min(speed + BALL_SPEEDUP, MAX_BALL_SPEED)
        angle = math.radians(MAX_BOUNCE_ANGLE) * hit_offset
        self.speed_x = speed * math.cos(angle) * direction
        self.speed_y = speed * math.sin(angle)
        # Push the ball outside the paddle to prevent repeated collisions
        if direction > 0:
            self.x = paddle_rect.right + 1
        else:
            self.x = paddle_rect.left - self.size - 1
    def off_screen_side(self):
        """Return 'left' or 'right' if the ball left the court, else None."""
        if self.x + self.size < 0:
            return 'left'
        if self.x > SCREEN_WIDTH:
            return 'right'
        return None
    def draw(self, screen):
        """Render the ball."""
        pygame.draw.rect(screen, WHITE, self.get_rect())