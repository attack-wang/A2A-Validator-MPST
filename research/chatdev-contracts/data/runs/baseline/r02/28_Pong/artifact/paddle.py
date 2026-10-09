'''
paddle.py
Paddle entity for the two-player Pong game.
A Paddle is a vertical bar owned by one player. It reads two keyboard
keys (up / down), moves accordingly, stays clamped inside the window
and knows how to render itself and report the relative impact point of
a colliding ball (used to compute the bounce angle).
'''
import pygame
import settings
class Paddle:
    """Vertical player-controlled paddle."""
    def __init__(self, side, up_key, down_key):
        """
        Create a paddle.
        :param side: "left" or "right" - fixes the starting x position.
        :param up_key: pygame key constant that moves the paddle up.
        :param down_key: pygame key constant that moves the paddle down.
        """
        self.side = side
        self.up_key = up_key
        self.down_key = down_key
        self.width = settings.PADDLE_WIDTH
        self.height = settings.PADDLE_HEIGHT
        self.speed = settings.PADDLE_SPEED
        if side == "left":
            self.x = settings.PADDLE_MARGIN
        else:
            self.x = settings.SCREEN_WIDTH - settings.PADDLE_MARGIN - self.width
        self.y = (settings.SCREEN_HEIGHT - self.height) // 2
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.color = (settings.COLOR_PADDLE_LEFT
                      if side == "left" else settings.COLOR_PADDLE_RIGHT)
    def reset(self):
        """Re-centre the paddle vertically (used when a match starts)."""
        self.y = (settings.SCREEN_HEIGHT - self.height) // 2
        self.rect.topleft = (self.x, self.y)
    def update(self):
        """Read the keyboard, move the paddle and clamp it to the window."""
        keys = pygame.key.get_pressed()
        dy = 0
        if keys[self.up_key]:
            dy -= self.speed
        if keys[self.down_key]:
            dy += self.speed
        if dy:
            self.y += dy
            self.y = max(0, min(settings.SCREEN_HEIGHT - self.height, self.y))
            self.rect.topleft = (self.x, self.y)
    def hit_offset(self, ball_rect):
        """
        Relative vertical offset of the ball's centre vs the paddle's
        centre, clamped to [-1, 1]. +1 = ball hit the very bottom of the
        paddle, -1 = the very top. Drives the bounce angle in Ball.
        """
        max_offset = (self.height + ball_rect.height) / 2
        offset = (ball_rect.centery - self.rect.centery) / max_offset
        return max(-1.0, min(1.0, offset))
    def draw(self, surface):
        """Render the paddle with rounded corners."""
        pygame.draw.rect(surface, self.color, self.rect, border_radius=6)