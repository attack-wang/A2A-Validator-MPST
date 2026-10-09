'''
ball.py
Defines the Ball class: movement, wall bouncing, angle-based paddle
reflection, out-of-bounds detection and rendering.
'''
import math
import random
import pygame
import constants as c
class Ball:
    '''The ball: moves, bounces off walls/paddles, resets after each point.'''
    def __init__(self):
        '''Create the ball and serve it in a random horizontal direction.'''
        self.size = c.BALL_SIZE
        self.rect = pygame.Rect(0, 0, self.size, self.size)
        self.base_speed = c.BALL_INITIAL_SPEED
        self.speed_x = 0.0
        self.speed_y = 0.0
        self.pos_x = 0.0
        self.pos_y = 0.0
        self.reset(random.choice([-1, 1]))
    def reset(self, serve_direction):
        '''Center the ball and serve toward serve_direction at a random angle.'''
        self.pos_x = c.WINDOW_WIDTH / 2
        self.pos_y = c.WINDOW_HEIGHT / 2
        self.base_speed = c.BALL_INITIAL_SPEED
        angle = random.uniform(-c.MAX_BOUNCE_ANGLE / 2, c.MAX_BOUNCE_ANGLE / 2)
        self.speed_x = self.base_speed * math.cos(angle) * serve_direction
        self.speed_y = self.base_speed * math.sin(angle)
        self.sync_rect()
    def sync_rect(self):
        '''Sync the integer collision rect with the float position.'''
        self.rect.center = (round(self.pos_x), round(self.pos_y))
    def update(self, left_paddle, right_paddle):
        '''Advance the ball one frame and resolve wall/paddle collisions.'''
        self.pos_x += self.speed_x
        self.pos_y += self.speed_y
        self.sync_rect()
        self._bounce_off_walls()
        self._bounce_off_paddle(left_paddle, going_right_after=True)
        self._bounce_off_paddle(right_paddle, going_right_after=False)
    def _bounce_off_walls(self):
        '''Bounce off the top and bottom window edges.'''
        half = self.size / 2
        if self.pos_y - half <= 0:
            self.pos_y = half
            self.speed_y = abs(self.speed_y)
        elif self.pos_y + half >= c.WINDOW_HEIGHT:
            self.pos_y = c.WINDOW_HEIGHT - half
            self.speed_y = -abs(self.speed_y)
        self.sync_rect()
    def _bounce_off_paddle(self, paddle, going_right_after):
        '''Reflect the ball only when it moves into the paddle it overlaps.'''
        paddle_rect = paddle.get_rect()
        if not self.rect.colliderect(paddle_rect):
            return
        if going_right_after and self.speed_x < 0:
            self.pos_x = paddle_rect.right + self.size / 2
            self._reflect(paddle_rect, going_right_after)
        elif not going_right_after and self.speed_x > 0:
            self.pos_x = paddle_rect.left - self.size / 2
            self._reflect(paddle_rect, going_right_after)
        self.sync_rect()
    def _reflect(self, paddle_rect, going_right_after):
        '''Set outgoing speed/angle from where the ball hit the paddle face.'''
        hit_pos = (self.pos_y - paddle_rect.centery) / (paddle_rect.height / 2)
        hit_pos = max(-1.0, min(1.0, hit_pos))
        self.base_speed = min(self.base_speed * c.BALL_SPEEDUP_FACTOR, c.MAX_BALL_SPEED)
        angle = hit_pos * c.MAX_BOUNCE_ANGLE
        direction = 1 if going_right_after else -1
        self.speed_x = self.base_speed * math.cos(angle) * direction
        self.speed_y = self.base_speed * math.sin(angle)
    def is_out_left(self):
        '''True when the ball fully crossed the left edge (right player scores).'''
        return self.pos_x + self.size / 2 < 0
    def is_out_right(self):
        '''True when the ball fully crossed the right edge (left player scores).'''
        return self.pos_x - self.size / 2 > c.WINDOW_WIDTH
    def draw(self, surface):
        '''Render the ball as a circle at its current position.'''
        pygame.draw.circle(surface, c.COLOR_BALL, self.rect.center, self.size // 2)