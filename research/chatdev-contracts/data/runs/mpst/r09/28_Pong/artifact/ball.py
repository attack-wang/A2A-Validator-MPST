'''
ball.py
Defines the Ball entity: movement, bouncing off the top/bottom edges,
angle-based reflection off paddles with a slight speed-up, and reset
(serve) after each point.
'''
import math
import random
import pygame
import settings
class Ball:
    """The ball that bounces between the paddles and off the screen edges."""
    def __init__(self):
        """Create the ball centered on screen and pick a random first serve."""
        self.size = settings.BALL_SIZE
        self.rect = pygame.Rect(0, 0, self.size, self.size)
        self.speed_x = 0.0
        self.speed_y = 0.0
        self.reset(serve_direction=random.choice((-1, 1)))
    def reset(self, serve_direction):
        """Center the ball and serve it toward `serve_direction` (+1 right, -1 left)."""
        self.rect.center = (settings.SCREEN_WIDTH // 2, settings.SCREEN_HEIGHT // 2)
        self.speed_x = settings.BALL_INITIAL_SPEED_X * serve_direction
        self.speed_y = settings.BALL_INITIAL_SPEED_Y * random.choice((-1, 1))
    def _bounce_off_paddle(self, paddle):
        """Reflect off a paddle, steering by the hit position and speeding up."""
        # Relative hit position on the paddle: -1 (top edge) .. +1 (bottom edge)
        offset = (self.rect.centery - paddle.rect.centery) / (paddle.rect.height / 2)
        offset = max(-1.0, min(1.0, offset))
        max_angle = math.radians(settings.BALL_MAX_BOUNCE_ANGLE)
        bounce_angle = offset * max_angle
        speed = math.hypot(self.speed_x, self.speed_y) * settings.BALL_SPEEDUP_FACTOR
        speed = min(speed, settings.BALL_MAX_SPEED)
        # Send the ball back toward the side it came from.
        direction = 1 if self.speed_x < 0 else -1
        self.speed_x = speed * math.cos(bounce_angle) * direction
        self.speed_y = speed * math.sin(bounce_angle)
        # Push the ball outside the paddle so it cannot get stuck inside.
        if direction == 1:
            self.rect.left = paddle.rect.right
        else:
            self.rect.right = paddle.rect.left
    def update(self, paddles):
        """
        Advance the ball one frame.
        Returns:
            None    -> ball still in play
            "left"  -> ball left the screen on the left (right player scores)
            "right" -> ball left the screen on the right (left player scores)
        """
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y
        # Bounce off the top and bottom edges.
        if self.rect.top <= 0:
            self.rect.top = 0
            self.speed_y = abs(self.speed_y)
        elif self.rect.bottom >= settings.SCREEN_HEIGHT:
            self.rect.bottom = settings.SCREEN_HEIGHT
            self.speed_y = -abs(self.speed_y)
        # Bounce off paddles (only when the ball is travelling toward them).
        for paddle in paddles:
            if not self.rect.colliderect(paddle.rect):
                continue
            moving_left = self.speed_x < 0
            is_left_paddle = paddle.rect.centerx < settings.SCREEN_WIDTH // 2
            if (is_left_paddle and moving_left) or (not is_left_paddle and not moving_left):
                self._bounce_off_paddle(paddle)
                break
        # Detect a missed ball.
        if self.rect.right <= 0:
            return "left"
        if self.rect.left >= settings.SCREEN_WIDTH:
            return "right"
        return None
    def draw(self, surface):
        """Render the ball as a circle."""
        pygame.draw.circle(surface, settings.COLOR_BALL, self.rect.center, self.size // 2)