'''
ball.py
Defines the Ball entity: the square ball that travels across the
playfield, bounces off the top/bottom walls and the paddles, and is
reset to the center after every point.
'''
import random
import pygame
import settings
class Ball:
    """Ball that bounces between paddles and off the top/bottom edges."""
    def __init__(self):
        self.size = settings.BALL_SIZE
        self.rect = pygame.Rect(0, 0, self.size, self.size)
        self.speed_x = 0.0
        self.speed_y = 0.0
        self.max_speed = settings.BALL_MAX_SPEED
        self.reset(direction=1)
    def reset(self, direction=None):
        """Place the ball at the center and (re)launch it.
        `direction` (+1/-1) sets the horizontal serve direction; when
        None a random direction is chosen.
        """
        self.rect.center = (settings.WIDTH // 2, settings.HEIGHT // 2)
        if direction is None:
            direction = random.choice([-1, 1])
        self.speed_x = settings.BALL_INITIAL_SPEED_X * direction
        self.speed_y = settings.BALL_INITIAL_SPEED_Y * random.choice([-1, 1])
    def update(self):
        """Move the ball by its current velocity."""
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y
    def bounce_top_bottom(self):
        """Reverse vertical direction (top/bottom wall hit)."""
        self.speed_y *= -1
    def bounce_paddle(self, paddle):
        """Reverse horizontal direction, nudge ball out of the paddle,
        speed up, and angle the ball based on the hit position."""
        if paddle.rect.centerx < settings.WIDTH // 2:      # left paddle
            self.rect.left = paddle.rect.right
            self.speed_x = abs(self.speed_x)
        else:                                              # right paddle
            self.rect.right = paddle.rect.left
            self.speed_x = -abs(self.speed_x)
        # Increase speed up to max
        if abs(self.speed_x) < self.max_speed:
            self.speed_x += settings.BALL_SPEED_INCREMENT * (1 if self.speed_x > 0 else -1)
        # Angle the ball based on where it struck the paddle
        offset = (self.rect.centery - paddle.rect.centery) / (paddle.rect.height / 2)
        offset = max(-1.0, min(1.0, offset))
        self.speed_y = settings.BALL_INITIAL_SPEED_Y * 2 * offset
        if abs(self.speed_y) < 1:                          # avoid a flat trajectory
            self.speed_y = random.choice([-1, 1])
    def draw(self, screen):
        pygame.draw.rect(screen, settings.WHITE, self.rect)