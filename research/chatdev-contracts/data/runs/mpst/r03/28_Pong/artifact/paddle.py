'''
paddle.py
Paddle entity for the two-player Pong game.
A paddle is a vertical rectangle that a player moves up and down.
It clamps itself inside the play field and knows how to check
collision with the ball.
'''
from settings import (SCREEN_WIDTH, SCREEN_HEIGHT, PADDLE_WIDTH,
                      PADDLE_HEIGHT, PADDLE_SPEED, PADDLE_MARGIN)
class Paddle:
    '''Vertical paddle controlled by one player.'''
    def __init__(self, side):
        '''Create a paddle; `side` is "left" or "right".'''
        self.side = side
        self.width = PADDLE_WIDTH
        self.height = PADDLE_HEIGHT
        self.speed = PADDLE_SPEED
        if side == "left":
            self.x = PADDLE_MARGIN
        else:
            self.x = SCREEN_WIDTH - PADDLE_MARGIN - PADDLE_WIDTH
        self.y = (SCREEN_HEIGHT - self.height) / 2
        self.moving_up = False
        self.moving_down = False
    # ------------------------------------------------- geometry helpers ----
    @property
    def top(self):
        '''Top edge y coordinate.'''
        return self.y
    @property
    def bottom(self):
        '''Bottom edge y coordinate.'''
        return self.y + self.height
    @property
    def left(self):
        '''Left edge x coordinate.'''
        return self.x
    @property
    def right(self):
        '''Right edge x coordinate.'''
        return self.x + self.width
    @property
    def center_y(self):
        '''Vertical centre of the paddle.'''
        return self.y + self.height / 2
    # -------------------------------------------------------- behaviour ----
    def update(self):
        '''Move the paddle according to the pressed keys and clamp it.'''
        if self.moving_up:
            self.y -= self.speed
        if self.moving_down:
            self.y += self.speed
        if self.y < 0:
            self.y = 0
        elif self.bottom > SCREEN_HEIGHT:
            self.y = SCREEN_HEIGHT - self.height
    def overlaps(self, ball):
        '''True when the ball's bounding box overlaps this paddle.'''
        return not (ball.right < self.left or ball.left > self.right or
                    ball.bottom < self.top or ball.top > self.bottom)