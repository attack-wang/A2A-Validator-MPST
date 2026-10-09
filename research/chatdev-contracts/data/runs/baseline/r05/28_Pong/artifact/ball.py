'''
ball.py
Defines the Ball class: the ball that travels between the two paddles.
Handles per-frame movement, bouncing off the top/bottom edges,
angle adjustment and speed-up on paddle hits, and resetting to the
center after each point.
'''
import math
import random
import pygame
import settings
class Ball:
    '''The ball that bounces between the paddles and off the walls.'''
    def __init__(self):
        '''Create the ball at the court center, served in a random direction.'''
        self.size = settings.BALL_SIZE
        self.max_speed = settings.BALL_MAX_SPEED
        self.reset()
    def get_rect(self):
        '''Return the pygame.Rect used for collision tests and drawing.'''
        return pygame.Rect(int(self.x), int(self.y), self.size, self.size)
    def reset(self, direction=None):
        '''
        Place the ball at the center of the court with fresh velocity.
        `direction` is -1 (serve left) or 1 (serve right); when None the
        serving side is chosen at random. Called after every point.
        '''
        if direction is None:
            direction = random.choice([-1, 1])
        self.x = (settings.SCREEN_WIDTH - self.size) / 2
        self.y = (settings.SCREEN_HEIGHT - self.size) / 2
        self.speed_x = settings.BALL_INITIAL_SPEED_X * direction
        self.speed_y = settings.BALL_INITIAL_SPEED_Y * random.choice([-1, 1])
    def move(self):
        '''Advance the ball one frame along its current velocity.'''
        self.x += self.speed_x
        self.y += self.speed_y
    def bounce_vertical(self):
        '''Reverse the vertical direction (bounce off top/bottom edges).'''
        self.speed_y = -self.speed_y
    def bounce_horizontal(self, paddle):
        '''Reverse the horizontal direction off a paddle, then tune the
        bounce angle by the hit position and increase the speed.'''
        self.speed_x = -self.speed_x
        self.adjust_angle(paddle)
        self.increase_speed()
    def adjust_angle(self, paddle):
        '''Steer the bounce based on where the ball struck the paddle:
        hitting near the top sends the ball upward, near the bottom downward.'''
        paddle_rect = paddle.get_rect()
        ball_rect = self.get_rect()
        # Relative hit position: -1.0 (paddle top) .. +1.0 (paddle bottom)
        hit_position = (ball_rect.centery - paddle_rect.centery) / (paddle_rect.height / 2)
        hit_position = max(-1.0, min(1.0, hit_position))
        bounce_angle = math.radians(hit_position * settings.MAX_BOUNCE_ANGLE)
        speed = math.hypot(self.speed_x, self.speed_y)
        direction = 1 if self.speed_x > 0 else -1  # post-bounce horizontal direction
        self.speed_x = direction * speed * math.cos(bounce_angle)
        self.speed_y = speed * math.sin(bounce_angle)
    def increase_speed(self):
        '''Speed the ball up slightly after each paddle hit, capped at max speed.'''
        current_speed = math.hypot(self.speed_x, self.speed_y)
        if current_speed < self.max_speed:
            new_speed = min(current_speed + settings.BALL_SPEED_INCREMENT, self.max_speed)
            scale = new_speed / current_speed
            self.speed_x *= scale
            self.speed_y *= scale
    def draw(self, screen):
        '''Render the ball as a rounded square onto the given screen surface.'''
        pygame.draw.ellipse(screen, settings.WHITE, self.get_rect())