'''
Ball class for the Pong game.
Encapsulates the ball's position, velocity and rendering. Provides
wall bouncing on the top/bottom edges, speed ramp-up after paddle
hits, and a reset routine used after every scored point.
'''
import math
import random
import pygame
import settings
class Ball:
    """Square ball that travels between the two paddles."""
    def __init__(self):
        """Create the ball and perform an initial random-direction reset."""
        self.size = settings.BALL_SIZE
        self.rect = pygame.Rect(0, 0, self.size, self.size)
        self.base_speed = settings.BALL_INITIAL_SPEED_X
        self.speed_x = 0.0
        self.speed_y = 0.0
        self.reset(direction=random.choice((-1, 1)))
    def reset(self, direction):
        """
        Center the ball and aim it toward `direction` (-1 = left, +1 = right).
        Speed is restored to its initial value and the vertical component
        is randomized so each serve is slightly different.
        """
        self.rect.center = (settings.WINDOW_WIDTH // 2, settings.WINDOW_HEIGHT // 2)
        self.base_speed = settings.BALL_INITIAL_SPEED_X
        angle = random.uniform(-settings.BALL_MAX_SERVE_ANGLE, settings.BALL_MAX_SERVE_ANGLE)
        self.speed_x = math.copysign(self.base_speed * math.cos(math.radians(angle)), direction)
        self.speed_y = self.base_speed * math.sin(math.radians(angle))
    def update(self):
        """
        Move the ball one frame and bounce off the top/bottom window edges.
        Horizontal edges are intentionally not handled here: leaving the
        playfield means a point was scored, which the Game class detects.
        """
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y
        if self.rect.top <= 0:
            self.rect.top = 0
            self.speed_y = abs(self.speed_y)
        elif self.rect.bottom >= settings.WINDOW_HEIGHT:
            self.rect.bottom = settings.WINDOW_HEIGHT
            self.speed_y = -abs(self.speed_y)
    def bounce_off_paddle(self, paddle, direction):
        """
        Reflect the ball off `paddle` (+1 = moving right afterwards, -1 = left).
        The outgoing angle depends on where the ball struck the paddle
        (edge hits deflect more), and the overall speed increases slightly
        with every hit up to a configured maximum.
        """
        paddle_center = paddle.rect.centery
        offset = (self.rect.centery - paddle_center) / (paddle.rect.height / 2)
        offset = max(-1.0, min(1.0, offset))
        speed = min(self.current_speed() + settings.BALL_SPEED_INCREMENT, settings.BALL_MAX_SPEED)
        angle = offset * settings.BALL_MAX_BOUNCE_ANGLE
        self.speed_x = math.copysign(speed * math.cos(math.radians(angle)), direction)
        self.speed_y = speed * math.sin(math.radians(angle))
        # Push the ball clear of the paddle so it does not re-collide.
        if direction > 0:
            self.rect.left = paddle.rect.right
        else:
            self.rect.right = paddle.rect.left
    def current_speed(self):
        """Return the ball's current speed magnitude."""
        return math.hypot(self.speed_x, self.speed_y)
    def draw(self, screen):
        """Render the ball as a square (rect) surface."""
        pygame.draw.rect(screen, settings.COLOR_BALL, self.rect)