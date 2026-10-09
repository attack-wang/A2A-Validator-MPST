'''
ball.py
Defines the Ball class: the square ball that travels across the screen,
bounces off the top/bottom walls and off the paddles, and can be reset
to the centre after a point is scored.
'''
import math
import random
import pygame
import settings
class Ball:
    """The game ball with position, velocity and bounce behaviour."""
    def __init__(self):
        self.rect = pygame.Rect(0, 0, settings.BALL_SIZE, settings.BALL_SIZE)
        self.speed = settings.BALL_INITIAL_SPEED
        self.velocity_x = 0.0
        self.velocity_y = 0.0
        self.reset(random.choice((-1, 1)))
    def reset(self, serve_direction):
        """Place the ball at the centre and aim it toward `serve_direction`."""
        self.rect.center = (settings.SCREEN_WIDTH // 2, settings.SCREEN_HEIGHT // 2)
        self.speed = settings.BALL_INITIAL_SPEED
        angle = random.uniform(-math.pi / 6, math.pi / 6)   # up to ~30 degrees
        self.velocity_x = serve_direction * self.speed * math.cos(angle)
        self.velocity_y = self.speed * math.sin(angle)
    def update(self):
        """Move the ball one frame and bounce off the top/bottom edges."""
        self.rect.x += int(round(self.velocity_x))
        self.rect.y += int(round(self.velocity_y))
        if self.rect.top <= 0:
            self.rect.top = 0
            self.velocity_y = abs(self.velocity_y)
        elif self.rect.bottom >= settings.SCREEN_HEIGHT:
            self.rect.bottom = settings.SCREEN_HEIGHT
            self.velocity_y = -abs(self.velocity_y)
    def bounce_off_paddle(self, paddle, direction):
        """
        Reflect the ball after hitting `paddle`.
        `direction` is +1 when the ball must travel rightwards (it hit the
        left paddle) and -1 when it must travel leftwards (right paddle).
        The deflection angle depends on where the ball struck the paddle,
        and every hit slightly increases the ball's speed.
        """
        # Relative hit position: -1 (paddle top) .. 0 (centre) .. +1 (bottom)
        hit_position = (self.rect.centery - paddle.rect.centery) / (paddle.rect.height / 2)
        hit_position = max(-1.0, min(1.0, hit_position))
        # Speed up a little on every hit, capped at BALL_MAX_SPEED.
        self.speed = min(self.speed + settings.BALL_SPEED_INCREMENT, settings.BALL_MAX_SPEED)
        max_angle = math.radians(settings.BALL_MAX_BOUNCE_ANGLE)
        angle = hit_position * max_angle
        self.velocity_x = direction * self.speed * math.cos(angle)
        self.velocity_y = self.speed * math.sin(angle)
        # Push the ball out of the paddle so it does not get stuck.
        if direction > 0:
            self.rect.left = paddle.rect.right
        else:
            self.rect.right = paddle.rect.left
    def draw(self, screen):
        pygame.draw.rect(screen, settings.FOREGROUND_COLOR, self.rect)