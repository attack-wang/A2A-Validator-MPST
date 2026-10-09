'''
Ball entity: movement, wall bounces, paddle deflection, and re-serving.
'''
import math
import random
import pygame
import settings
class Ball:
    '''The ball: moves, bounces off top/bottom walls, and re-serves after each point.'''
    def __init__(self):
        '''Create the ball parked at center, ready to serve toward the right.'''
        self.size = settings.BALL_DIAMETER
        self.speed = settings.BALL_INITIAL_SPEED
        self.x = 0.0
        self.y = 0.0
        self.velocity = [0.0, 0.0]
        self.serving = True
        self.serve_direction = 1.0
        self.rect = pygame.Rect(0, 0, self.size, self.size)
        self.reset(direction=1)
    def reset(self, direction=1):
        '''Center the ball and hold it until the next serve toward `direction` (+1 right, -1 left).'''
        self.x = (settings.SCREEN_WIDTH - self.size) / 2.0
        self.y = (settings.SCREEN_HEIGHT - self.size) / 2.0
        self.speed = settings.BALL_INITIAL_SPEED
        self.velocity = [0.0, 0.0]
        self.serving = True
        self.serve_direction = 1.0 if direction >= 0 else -1.0
        self._sync_rect()
    def is_serving(self):
        '''True while the ball is parked at center waiting for the serve timer.'''
        return self.serving
    def launch(self):
        '''Start moving toward serve_direction with a random vertical angle.'''
        max_angle = math.radians(settings.BALL_MAX_BOUNCE_ANGLE)
        angle = random.uniform(-max_angle, max_angle)
        self.velocity[0] = self.serve_direction * self.speed * math.cos(angle)
        self.velocity[1] = self.speed * math.sin(angle)
        self.serving = False
    def update(self, dt):
        '''Advance the ball in small sub-steps (anti-tunneling) and bounce off top/bottom edges.'''
        distance = self.speed * dt
        max_step = max(self.size * 0.5, 1.0)
        steps = max(1, int(math.ceil(distance / max_step)))
        step_dt = dt / steps
        for _ in range(steps):
            self.x += self.velocity[0] * step_dt
            self.y += self.velocity[1] * step_dt
            self._bounce_off_walls()
        self._sync_rect()
    def _bounce_off_walls(self):
        '''Reflect vertically off the top and bottom edges.'''
        if self.y <= 0.0:
            self.y = 0.0
            self.velocity[1] = abs(self.velocity[1])
        elif self.y >= settings.SCREEN_HEIGHT - self.size:
            self.y = settings.SCREEN_HEIGHT - self.size
            self.velocity[1] = -abs(self.velocity[1])
    def _sync_rect(self):
        '''Keep the integer collision rect aligned with the float position.'''
        self.rect.x = int(round(self.x))
        self.rect.y = int(round(self.y))
    def bounce_off_paddle(self, paddle):
        '''Deflect off a paddle; angle depends on hit position, speed grows on every hit.'''
        if self.rect.centerx < paddle.rect.centerx:
            # Hit the left paddle: push the ball out to its left, send it right.
            self.rect.right = paddle.rect.left
            new_direction = 1.0
        else:
            # Hit the right paddle: push the ball out to its right, send it left.
            self.rect.left = paddle.rect.right
            new_direction = -1.0
        self.x = float(self.rect.x)
        offset = (self.rect.centery - paddle.rect.centery) / (paddle.rect.height / 2.0)
        offset = max(-1.0, min(1.0, offset))
        angle = offset * math.radians(settings.BALL_MAX_BOUNCE_ANGLE)
        self.speed = min(self.speed * settings.BALL_SPEEDUP, settings.BALL_MAX_SPEED)
        self.velocity[0] = new_direction * self.speed * math.cos(angle)
        self.velocity[1] = self.speed * math.sin(angle)
    def draw(self, surface):
        '''Render the ball as a circle.'''
        pygame.draw.circle(surface, settings.COLOR_BALL, self.rect.center, self.size // 2)