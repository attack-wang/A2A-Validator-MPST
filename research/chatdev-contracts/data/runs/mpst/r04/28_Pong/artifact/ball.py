'''
ball.py
Defines the Ball class with movement, edge bouncing, and reset logic.
'''
import math
import random
import pygame
import settings
class Ball:
    '''The game ball: moves, bounces off top/bottom edges, resets after points.'''
    def __init__(self):
        self.size = settings.BALL_SIZE
        self.rect = pygame.Rect(0, 0, self.size, self.size)
        self.x = 0.0  # float position for smooth movement (fixes int truncation bug)
        self.y = 0.0
        self.speed_x = 0.0
        self.speed_y = 0.0
        self.serve_timer = 0
        self.reset(direction=random.choice([-1, 1]))
    def reset(self, direction):
        '''Center the ball and serve it toward the given horizontal direction.'''
        self.x = (settings.SCREEN_WIDTH - self.size) / 2
        self.y = (settings.SCREEN_HEIGHT - self.size) / 2
        self.rect.topleft = (int(self.x), int(self.y))
        self.speed_x = settings.BALL_INITIAL_SPEED_X * direction
        self.speed_y = random.uniform(-settings.BALL_INITIAL_SPEED_Y,
                                      settings.BALL_INITIAL_SPEED_Y)
        self.serve_timer = settings.SERVE_DELAY_FRAMES
    def update(self):
        '''Move the ball (after serve delay) and bounce off top/bottom edges.'''
        if self.serve_timer > 0:
            self.serve_timer -= 1
            return
        self.x += self.speed_x
        self.y += self.speed_y
        if self.y < 0:  # bounce off top edge
            self.y = 0
            self.speed_y = abs(self.speed_y)
        if self.y > settings.SCREEN_HEIGHT - self.size:  # bounce off bottom edge
            self.y = settings.SCREEN_HEIGHT - self.size
            self.speed_y = -abs(self.speed_y)
        self.rect.topleft = (int(self.x), int(self.y))
    def bounce_off_paddle(self, paddle):
        '''Bounce off a paddle, steering by hit position and speeding up slightly.'''
        # Direction the ball should travel after the bounce (away from paddle)
        direction = 1 if self.speed_x < 0 else -1
        # Normalized hit offset: -1 (paddle top) .. 1 (paddle bottom)
        offset = (self.rect.centery - paddle.rect.centery) / (paddle.rect.height / 2)
        offset = max(-1.0, min(1.0, offset))
        # Current speed plus a small increment, capped at the maximum
        speed = min(math.hypot(self.speed_x, self.speed_y) + settings.BALL_SPEED_INCREMENT,
                    settings.BALL_MAX_SPEED)
        # Steer the ball by the hit offset (max vertical angle)
        angle = offset * math.radians(settings.MAX_BOUNCE_ANGLE)
        self.speed_x = speed * math.cos(angle) * direction
        self.speed_y = speed * math.sin(angle)
        # Nudge the ball just outside the paddle so it does not stick
        if direction == 1:
            self.x = paddle.rect.right + 1
        else:
            self.x = paddle.rect.left - self.size - 1
        self.rect.topleft = (int(self.x), int(self.y))
    def draw(self, screen):
        '''Render the ball.'''
        pygame.draw.rect(screen, settings.WHITE, self.rect)