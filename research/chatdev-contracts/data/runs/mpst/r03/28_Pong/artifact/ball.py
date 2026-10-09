'''
ball.py
Ball entity for the two-player Pong game.
The ball travels across the field, bounces off the top and bottom
edges, is deflected by the paddles depending on the hit position and
is re-served with a short countdown after every point.
'''
import math
import random
from settings import (SCREEN_WIDTH, SCREEN_HEIGHT, BALL_RADIUS,
                      BALL_INITIAL_SPEED, BALL_SPEED_INCREMENT,
                      BALL_MAX_SPEED, MAX_BOUNCE_ANGLE, SERVE_DELAY_FRAMES)
class Ball:
    '''The bouncing ball of the Pong game.'''
    def __init__(self):
        self.radius = BALL_RADIUS
        self.x = SCREEN_WIDTH / 2
        self.y = SCREEN_HEIGHT / 2
        self.vx = 0.0
        self.vy = 0.0
        self.speed = BALL_INITIAL_SPEED
        self.serve_timer = 0
        self.reset(random.choice([-1, 1]))
    # ------------------------------------------------- geometry helpers ----
    @property
    def left(self):
        '''Left edge x coordinate.'''
        return self.x - self.radius
    @property
    def right(self):
        '''Right edge x coordinate.'''
        return self.x + self.radius
    @property
    def top(self):
        '''Top edge y coordinate.'''
        return self.y - self.radius
    @property
    def bottom(self):
        '''Bottom edge y coordinate.'''
        return self.y + self.radius
    # -------------------------------------------------------- behaviour ----
    def reset(self, direction):
        '''Centre the ball and start the serve countdown toward `direction`.'''
        self.x = SCREEN_WIDTH / 2
        self.y = SCREEN_HEIGHT / 2
        self.speed = BALL_INITIAL_SPEED
        angle = math.radians(random.uniform(-MAX_BOUNCE_ANGLE / 2,
                                            MAX_BOUNCE_ANGLE / 2))
        self.vx = direction * self.speed * math.cos(angle)
        self.vy = self.speed * math.sin(angle)
        self.serve_timer = SERVE_DELAY_FRAMES
    def update(self, paddles):
        '''
        Advance the ball by one frame.
        Returns "left" or "right" when that player scores a point
        (the opponent missed), otherwise None.
        '''
        if self.serve_timer > 0:
            self.serve_timer -= 1
            return None
        self.x += self.vx
        self.y += self.vy
        # bounce off the top and bottom edges
        if self.top < 0:
            self.y = self.radius
            self.vy = abs(self.vy)
        elif self.bottom > SCREEN_HEIGHT:
            self.y = SCREEN_HEIGHT - self.radius
            self.vy = -abs(self.vy)
        # deflect off the paddles
        for paddle in paddles:
            if paddle.overlaps(self):
                if paddle.side == "left" and self.vx < 0:
                    self._bounce_off(paddle)
                elif paddle.side == "right" and self.vx > 0:
                    self._bounce_off(paddle)
        # a point is scored when the ball leaves the field horizontally
        if self.right < 0:
            return "right"
        if self.left > SCREEN_WIDTH:
            return "left"
        return None
    def _bounce_off(self, paddle):
        '''Reflect the ball and steer it based on where it hit the paddle.'''
        # relative hit position: -1 at the top edge, +1 at the bottom edge
        rel = (self.y - paddle.center_y) / (paddle.height / 2)
        rel = max(-1.0, min(1.0, rel))
        angle = math.radians(rel * MAX_BOUNCE_ANGLE)
        # every hit makes the ball a bit faster (up to the cap)
        self.speed = min(self.speed + BALL_SPEED_INCREMENT, BALL_MAX_SPEED)
        if paddle.side == "left":
            self.vx = abs(self.speed * math.cos(angle))
            self.x = paddle.right + self.radius
        else:
            self.vx = -abs(self.speed * math.cos(angle))
            self.x = paddle.left - self.radius
        self.vy = self.speed * math.sin(angle)