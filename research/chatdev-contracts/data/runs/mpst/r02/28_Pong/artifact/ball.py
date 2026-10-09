'''
Ball module.
Defines the Ball entity: float-based velocity movement, bouncing off the
top/bottom edges, angled deflection off paddles with a slight speed-up,
and re-centering after each point with a delayed launch (serve).
Rendering is done on a tkinter Canvas (Python standard library only).
'''
import math
import random
from settings import (
    BALL_SIZE,
    BALL_BASE_SPEED,
    BALL_MAX_SPEED,
    BALL_SPEEDUP_FACTOR,
    BALL_MAX_BOUNCE_ANGLE,
    COLOR_BALL,
    SCREEN_WIDTH,
    SCREEN_HEIGHT,
)
class Ball:
    """The ball that bounces between the two paddles."""
    def __init__(self):
        """Create the ball centred and stationary, waiting for the first serve."""
        self.size = BALL_SIZE
        self.speed = BALL_BASE_SPEED
        self.dx = 0.0
        self.dy = 0.0
        self.reset_position()
    def reset_position(self):
        """Center the ball and stop it while waiting for the next serve."""
        self.speed = BALL_BASE_SPEED
        self.dx = 0.0
        self.dy = 0.0
        self.x = SCREEN_WIDTH / 2 - BALL_SIZE / 2
        self.y = SCREEN_HEIGHT / 2 - BALL_SIZE / 2
    def launch(self, direction):
        """Launch the ball from the centre toward `direction`
        (-1 = toward the left player, +1 = toward the right player)."""
        self.speed = BALL_BASE_SPEED
        angle = math.radians(random.uniform(-45, 45))
        self.dx = direction * math.cos(angle) * self.speed
        self.dy = math.sin(angle) * self.speed
    def update(self):
        """Move the ball and bounce it off the top and bottom edges."""
        self.x += self.dx
        self.y += self.dy
        if self.y <= 0:
            self.y = 0.0
            self.dy = abs(self.dy)
        elif self.y + self.size >= SCREEN_HEIGHT:
            self.y = float(SCREEN_HEIGHT - self.size)
            self.dy = -abs(self.dy)
    def rect(self):
        """Return the ball rectangle as (x1, y1, x2, y2)."""
        return (self.x, self.y, self.x + self.size, self.y + self.size)
    def centery(self):
        """Vertical centre of the ball."""
        return self.y + self.size / 2
    def bounce_off_paddle(self, paddle):
        """Deflect the ball off `paddle`, aiming away from it.
        The vertical hit position controls the bounce angle and the
        ball slightly speeds up to raise tension during long rallies."""
        # Horizontal direction away from the paddle.
        direction = 1 if paddle.centerx() < SCREEN_WIDTH // 2 else -1
        # Relative hit position: -1 (paddle top) .. +1 (paddle bottom).
        rel = (self.centery() - paddle.centery()) / (paddle.height / 2)
        rel = max(-1.0, min(1.0, rel))
        # Speed up (capped) and compute the new velocity components.
        self.speed = min(self.speed * BALL_SPEEDUP_FACTOR, BALL_MAX_SPEED)
        angle = math.radians(rel * BALL_MAX_BOUNCE_ANGLE)
        self.dx = direction * math.cos(angle) * self.speed
        self.dy = math.sin(angle) * self.speed
        # Push the ball out of the paddle so it does not stick.
        if direction == 1:
            self.x = paddle.x + paddle.width
        else:
            self.x = paddle.x - self.size
    def off_left(self):
        """True when the ball has fully left the playfield on the left."""
        return self.x + self.size < 0
    def off_right(self):
        """True when the ball has fully left the playfield on the right."""
        return self.x > SCREEN_WIDTH
    def draw(self, canvas):
        """Render the ball as a circle on the tkinter canvas."""
        canvas.create_oval(
            self.x, self.y, self.x + self.size, self.y + self.size,
            fill=COLOR_BALL, outline="",
        )