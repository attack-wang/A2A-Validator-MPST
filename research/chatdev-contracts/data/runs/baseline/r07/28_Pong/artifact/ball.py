'''
ball.py
Defines the Ball class: the ball with movement, wall bounces, and paddle collisions.
'''
import math
import random
import pygame
from constants import (BALL_SIZE, BALL_INITIAL_SPEED, BALL_SPEED_INCREMENT,
                       BALL_MAX_SPEED, BALL_MAX_BOUNCE_ANGLE,
                       WINDOW_WIDTH, WINDOW_HEIGHT, COLOR_BALL)
class Ball:
    '''The game ball: moves around, bounces off walls and paddles.'''
    def __init__(self):
        '''Create the ball at the center of the window.'''
        self.size = BALL_SIZE
        self.speed = BALL_INITIAL_SPEED
        self.vx = 0.0
        self.vy = 0.0
        self.reset(direction=1)
    def reset(self, direction):
        '''Place the ball at center and serve it toward `direction` (+1 right, -1 left).'''
        self.x = WINDOW_WIDTH / 2 - self.size / 2
        self.y = WINDOW_HEIGHT / 2 - self.size / 2
        self.speed = BALL_INITIAL_SPEED
        angle = random.uniform(-30, 30)  # slight random serve angle
        self.vx = direction * self.speed * math.cos(math.radians(angle))
        self.vy = self.speed * math.sin(math.radians(angle))
    def get_rect(self):
        '''Return the pygame.Rect used for collision and drawing.'''
        return pygame.Rect(int(self.x), int(self.y), self.size, self.size)
    def update(self, paddles):
        '''
        Move the ball one frame: bounce off top/bottom walls, bounce off paddles
        (adjusting the bounce angle by the hit offset), and slightly speed up
        on each paddle hit.
        Returns nothing; scoring is detected by the Game via `out_of_bounds`.
        '''
        self.x += self.vx
        self.y += self.vy
        # Bounce off top and bottom edges
        if self.y <= 0:
            self.y = 0
            self.vy = abs(self.vy)
        elif self.y >= WINDOW_HEIGHT - self.size:
            self.y = WINDOW_HEIGHT - self.size
            self.vy = -abs(self.vy)
        # Collisions with paddles
        for paddle in paddles:
            if self.get_rect().colliderect(paddle.get_rect()):
                self._bounce_off_paddle(paddle)
    def _bounce_off_paddle(self, paddle):
        '''Reflect the ball off a paddle, steering by the vertical hit offset.'''
        rect = self.get_rect()
        p_rect = paddle.get_rect()
        # Determine whether the ball came from the left or right side
        if self.vx > 0 and rect.right >= p_rect.left and rect.left < p_rect.left:
            # Moving right, hit the paddle's left face
            self.x = p_rect.left - self.size
            hit_offset = self._hit_offset(p_rect)
            self._set_velocity(direction=-1, hit_offset=hit_offset)
        elif self.vx < 0 and rect.left <= p_rect.right and rect.right > p_rect.right:
            # Moving left, hit the paddle's right face
            self.x = p_rect.right
            hit_offset = self._hit_offset(p_rect)
            self._set_velocity(direction=1, hit_offset=hit_offset)
    def _hit_offset(self, p_rect):
        '''Return the vertical hit position on the paddle in [-1, 1] (center = 0).'''
        ball_center_y = self.y + self.size / 2
        paddle_center_y = p_rect.y + p_rect.height / 2
        offset = (ball_center_y - paddle_center_y) / (p_rect.height / 2)
        return max(-1.0, min(1.0, offset))
    def _set_velocity(self, direction, hit_offset):
        '''Recompute velocity after a paddle hit: reflect horizontally, steer vertically.'''
        # Increase speed up to the cap
        self.speed = min(self.speed + BALL_SPEED_INCREMENT, BALL_MAX_SPEED)
        angle = hit_offset * BALL_MAX_BOUNCE_ANGLE
        self.vx = direction * self.speed * math.cos(math.radians(angle))
        self.vy = self.speed * math.sin(math.radians(angle))
    def out_of_bounds(self):
        '''
        Return 0 while the ball is in play, -1 if it exited the left edge
        (right player scores), or +1 if it exited the right edge (left player scores).
        '''
        if self.x + self.size < 0:
            return -1
        if self.x > WINDOW_WIDTH:
            return 1
        return 0
    def draw(self, surface):
        '''Render the ball onto the given surface.'''
        pygame.draw.rect(surface, COLOR_BALL, self.get_rect())