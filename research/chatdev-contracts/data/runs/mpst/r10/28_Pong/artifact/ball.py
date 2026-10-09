'''
Ball module: defines the single, float-based Ball used in the Pong game.
The ball moves with sub-pixel precision (so fractional speed increments are
not lost), bounces off the top/bottom edges, bounces off paddles with
angle control and capped speed-up, and resets to center after each point.
'''
import pygame
import random
import settings
class Ball:
    '''The ball that bounces between paddles and off top/bottom edges.'''
    def __init__(self):
        '''Initialize a centered ball and serve it to the right.'''
        self.size = settings.BALL_SIZE
        self.pos_x = 0.0
        self.pos_y = 0.0
        self.speed_x = 0.0
        self.speed_y = 0.0
        self.rect = pygame.Rect(0, 0, self.size, self.size)
        self.reset(direction=1)
    def reset(self, direction):
        '''Center the ball and serve toward `direction` (+1 right, -1 left).'''
        self.pos_x = settings.SCREEN_WIDTH / 2 - self.size / 2
        self.pos_y = settings.SCREEN_HEIGHT / 2 - self.size / 2
        self.speed_x = settings.BALL_INITIAL_SPEED_X * direction
        self.speed_y = random.choice([-1, 1]) * settings.BALL_INITIAL_SPEED_Y
        self._sync_rect()
    def _sync_rect(self):
        '''Synchronize the integer drawing rect with the float position.'''
        self.rect.topleft = (round(self.pos_x), round(self.pos_y))
    def update(self):
        '''Move the ball and bounce off the top/bottom edges.'''
        self.pos_x += self.speed_x
        self.pos_y += self.speed_y
        # Top/bottom bounce (clamped so the ball never leaves the court)
        if self.pos_y <= 0:
            self.pos_y = 0
            self.speed_y = abs(self.speed_y)
        elif self.pos_y + self.size >= settings.SCREEN_HEIGHT:
            self.pos_y = settings.SCREEN_HEIGHT - self.size
            self.speed_y = -abs(self.speed_y)
        self._sync_rect()
    def bounce_off_paddle(self, paddle):
        '''Reverse direction, angle by hit position, and speed up (capped).
        The outgoing horizontal speed is the incoming speed plus
        BALL_SPEED_INCREMENT, capped at BALL_MAX_SPEED. The vertical speed
        is scaled by where the ball struck the paddle, giving players
        angle control. A minimum vertical speed prevents near-horizontal
        stalemates.
        '''
        # Determine hit position relative to paddle center, clamped to [-1, 1]
        hit_offset = max(-1.0, min(1.0,
            (self.rect.centery - paddle.rect.centery) / (paddle.height / 2)))
        # Reposition the ball just outside the paddle to avoid re-collision
        if self.speed_x > 0:
            self.pos_x, direction = paddle.rect.left - self.size, -1
        else:
            self.pos_x, direction = paddle.rect.right, 1
        # Speed up, capped at BALL_MAX_SPEED
        magnitude = min(abs(self.speed_x) + settings.BALL_SPEED_INCREMENT,
                        settings.BALL_MAX_SPEED)
        self.speed_x = direction * magnitude
        # Adjust vertical speed based on where it hit
        self.speed_y = hit_offset * magnitude * 0.75
        if abs(self.speed_y) < 1.0:
            self.speed_y = random.choice([-1, 1]) * 1.5
        self._sync_rect()
    def draw(self, screen):
        '''Render the ball onto the given surface.'''
        pygame.draw.rect(screen, settings.WHITE, self.rect)