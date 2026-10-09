'''
ball.py
Defines the Ball entity.
The ball travels with a constant speed magnitude; its direction changes
when it bounces off the top/bottom walls or is deflected by a paddle.
After a point is scored the ball is reset to the middle of the field and
re-served after a short delay.
'''
import math
import random
import pygame
import settings
class Ball:
    '''The ball that bounces between the two paddles.'''
    def __init__(self):
        self.rect = pygame.Rect(0, 0, settings.BALL_SIZE, settings.BALL_SIZE)
        self.speed = settings.BALL_INITIAL_SPEED
        self.velocity_x = 0.0
        self.velocity_y = 0.0
        self.serve_timer = 0
        self.serve_direction = random.choice((-1, 1))
        self.reset(self.serve_direction)
    def launch(self):
        '''
        Start moving after the serve delay has elapsed.
        The vertical component is chosen randomly; the horizontal component
        is derived via sqrt(speed^2 - vy^2) so that the overall speed
        magnitude exactly equals self.speed (BALL_INITIAL_SPEED at serve).
        '''
        vy = random.uniform(-settings.BALL_INITIAL_VY, settings.BALL_INITIAL_VY)
        vx_component = math.sqrt(max(self.speed ** 2 - vy ** 2, 0.0))
        self.velocity_x = self.serve_direction * vx_component
        self.velocity_y = vy
    def reset(self, serve_direction):
        '''
        Place the ball back in the centre and freeze it.
        serve_direction: +1 -> ball will travel towards the right player,
                         -1 -> ball will travel towards the left player.
        '''
        self.serve_direction = serve_direction
        self.rect.center = (settings.SCREEN_WIDTH // 2, settings.SCREEN_HEIGHT // 2)
        self.speed = settings.BALL_INITIAL_SPEED
        self.velocity_x = 0.0
        self.velocity_y = 0.0
        self.serve_timer = settings.SERVE_DELAY_FRAMES
    def update(self):
        '''
        Advance the ball one frame.
        While the serve timer is running the ball stays still; once the
        timer expires the ball is launched.  While in flight the ball
        bounces off the top and bottom edges of the playfield.
        '''
        if self.serve_timer > 0:
            self.serve_timer -= 1
            if self.serve_timer == 0:
                self.launch()
            return
        self.rect.x += self.velocity_x
        self.rect.y += self.velocity_y
        # Bounce off the top edge
        if self.rect.top <= 0:
            self.rect.top = 0
            self.velocity_y = abs(self.velocity_y)
        # Bounce off the bottom edge
        if self.rect.bottom >= settings.SCREEN_HEIGHT:
            self.rect.bottom = settings.SCREEN_HEIGHT
            self.velocity_y = -abs(self.velocity_y)
    def bounce_off_paddle(self, paddle):
        '''
        Deflect the ball after hitting a paddle.
        The outgoing angle depends on where the ball hit the paddle:
        hitting near the edge produces a steep angle, hitting the middle
        produces a flat angle.  The overall speed increases slightly with
        every hit (up to a maximum) so rallies get progressively faster.
        '''
        # Where did the ball hit the paddle?  -1 = top edge, 0 = centre, 1 = bottom edge
        relative_intersect = (paddle.rect.centery - self.rect.centery) / (paddle.rect.height / 2)
        relative_intersect = max(-1.0, min(1.0, relative_intersect))
        bounce_angle = math.radians(relative_intersect * settings.MAX_BOUNCE_ANGLE)
        # Speed up a little, but never exceed the configured maximum.
        self.speed = min(self.speed + settings.BALL_SPEED_UP, settings.BALL_MAX_SPEED)
        if paddle.side == 'left':
            direction = 1   # ball leaves the left paddle travelling right
        else:
            direction = -1  # ball leaves the right paddle travelling left
        self.velocity_x = direction * self.speed * math.cos(bounce_angle)
        self.velocity_y = -self.speed * math.sin(bounce_angle)
        # Push the ball out of the paddle so it does not get stuck inside.
        if paddle.side == 'left':
            self.rect.left = paddle.rect.right
        else:
            self.rect.right = paddle.rect.left
    def draw(self, surface):
        '''Render the ball on the given surface.'''
        pygame.draw.rect(surface, settings.COLOR_BALL, self.rect, border_radius=3)