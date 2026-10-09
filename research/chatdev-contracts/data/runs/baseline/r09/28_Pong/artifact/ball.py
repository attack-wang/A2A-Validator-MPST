'''
ball.py
Defines the Ball class: the ball that bounces between the two paddles
and off the top/bottom edges. Handles serve delays, edge bounces,
paddle deflection angles and the speed-up during a rally.
'''
import random
import pygame
import settings
class Ball:
    '''The bouncing ball of the Pong game.'''
    def __init__(self):
        '''Create the ball at the center of the playfield and serve it.'''
        self.size = settings.BALL_SIZE
        self.max_speed = settings.BALL_MAX_SPEED
        self.speed_increment = settings.BALL_SPEED_INCREMENT
        self.max_deflection = settings.MAX_DEFLECTION
        self.serve_delay = settings.SERVE_DELAY_FRAMES
        self.wait = 0
        self.reset(random.choice((-1, 1)))
    def reset(self, direction):
        '''
        Place the ball at the center and serve it toward `direction`
        (-1 serves left, +1 serves right) after a short delay.
        '''
        self.x = settings.SCREEN_WIDTH / 2 - self.size / 2
        self.y = settings.SCREEN_HEIGHT / 2 - self.size / 2
        self.speed_x = settings.BALL_INITIAL_SPEED_X * direction
        self.speed_y = random.choice((-1, 1)) * settings.BALL_INITIAL_SPEED_Y
        self.wait = self.serve_delay
        self.rect = pygame.Rect(int(self.x), int(self.y), self.size, self.size)
    def bounce_x(self):
        '''Reverse horizontal direction and speed up slightly (rally effect).'''
        self.speed_x = -self.speed_x
        if abs(self.speed_x) < self.max_speed:
            step = self.speed_increment if self.speed_x > 0 else -self.speed_increment
            self.speed_x += step
    def bounce_y(self):
        '''Reverse vertical direction (used for top/bottom edge bounces).'''
        self.speed_y = -self.speed_y
    def deflect(self, hit_offset):
        '''
        Bounce off a paddle. `hit_offset` is in [-1, 1] and describes where
        the ball struck the paddle (-1 = top edge, +1 = bottom edge); it
        sets the outgoing vertical speed so players can aim the ball.
        '''
        self.speed_y = hit_offset * self.max_deflection
        if abs(self.speed_y) < 1.0:
            # Nearly centered hit: add a small nudge so the ball never
            # travels in a perfectly flat, endless line.
            self.speed_y = random.choice((-1, 1)) * 2.0
        self.bounce_x()
    def update(self):
        '''Move the ball one frame, bouncing off the top and bottom edges.'''
        if self.wait > 0:
            self.wait -= 1
            return
        self.x += self.speed_x
        self.y += self.speed_y
        if self.y <= 0:
            self.y = 0
            self.bounce_y()
        elif self.y + self.size >= settings.SCREEN_HEIGHT:
            self.y = settings.SCREEN_HEIGHT - self.size
            self.bounce_y()
        self.rect.topleft = (int(self.x), int(self.y))
    def draw(self, surface):
        '''Render the ball onto the given surface.'''
        pygame.draw.rect(surface, settings.WHITE, self.rect)