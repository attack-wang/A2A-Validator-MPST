'''
ball.py
Ball entity: movement, wall bounces, paddle bounces and rendering.
The ball travels with a normalized velocity vector, reflects off the
top/bottom edges, deflects vertically depending on where it strikes a
paddle, and gains speed on every paddle hit (capped for playability).
'''
import math
import random
import pygame
import settings
class Ball:
    """Ball with float-precision movement, wall/paddle bounces and rendering."""
    def __init__(self):
        """Create the ball and serve it in a random horizontal direction."""
        self.size = settings.BALL_SIZE
        self.base_speed = settings.BALL_BASE_SPEED
        self.max_speed = settings.BALL_MAX_SPEED
        self.speed = self.base_speed
        self.x = 0.0
        self.y = 0.0
        self.dx = 0.0
        self.dy = 0.0
        self.rect = pygame.Rect(0, 0, self.size, self.size)
        self.reset(random.choice([-1, 1]))
    def reset(self, serve_direction):
        """Re-centre the ball, restore base speed and serve toward serve_direction."""
        self.speed = self.base_speed
        self.x = (settings.SCREEN_WIDTH - self.size) / 2
        self.y = (settings.SCREEN_HEIGHT - self.size) / 2
        angle = random.uniform(-0.5, 0.5)  # vertical slope factor
        self.dx = serve_direction
        self.dy = angle
        self._normalize()
        self._sync_rect()
    def _normalize(self):
        """Scale (dx, dy) so its magnitude equals the current speed."""
        magnitude = math.hypot(self.dx, self.dy)
        if magnitude == 0:
            self.dx, self.dy = 1.0, 0.0
            magnitude = 1.0
        self.dx = self.dx / magnitude * self.speed
        self.dy = self.dy / magnitude * self.speed
    def bounce_off_paddle(self, offset):
        """Reverse horizontal direction, deflect vertically by hit offset and speed up."""
        self.dx = -self.dx
        self.dy = offset * settings.BALL_ANGLE_FACTOR
        self.speed = min(self.speed + settings.BALL_SPEED_INCREMENT, self.max_speed)
        self._normalize()
    def bounce_vertical(self):
        """Reflect the ball off the top/bottom edge."""
        self.dy = -self.dy
    def update(self):
        """Move the ball one frame and bounce off the top/bottom edges."""
        self.x += self.dx
        self.y += self.dy
        if self.y <= 0:
            self.y = 0
            self.bounce_vertical()
        elif self.y >= settings.SCREEN_HEIGHT - self.size:
            self.y = settings.SCREEN_HEIGHT - self.size
            self.bounce_vertical()
        self._sync_rect()
    def set_position(self, x, y):
        """Place the ball at the given float coordinates."""
        self.x = float(x)
        self.y = float(y)
        self._sync_rect()
    def _sync_rect(self):
        """Copy the float position into the integer collision rect."""
        self.rect.topleft = (int(round(self.x)), int(round(self.y)))
    def draw(self, surface):
        """Render the ball as a rounded square (visually a circle)."""
        pygame.draw.rect(surface, settings.COLOR_BALL, self.rect,
                         border_radius=self.size // 2)