'''
paddle.py
Defines the Paddle entity: a vertical bar controlled by one player that
moves up and down, stays inside the playfield and can collide with the ball.
'''
import pygame
import settings
class Paddle:
    """A vertical paddle moved up and down by a single player."""
    def __init__(self, side):
        """Create a paddle for `side` ("left" or "right"), centered vertically."""
        self.side = side
        self.width = settings.PADDLE_WIDTH
        self.height = settings.PADDLE_HEIGHT
        self.speed = settings.PADDLE_SPEED
        if side == "left":
            self.x = settings.PADDLE_MARGIN
            self.color = settings.COLOR_PADDLE_LEFT
            self.up_key = settings.CONTROLS_LEFT["up"]
            self.down_key = settings.CONTROLS_LEFT["down"]
        else:
            self.x = settings.SCREEN_WIDTH - settings.PADDLE_MARGIN - self.width
            self.color = settings.COLOR_PADDLE_RIGHT
            self.up_key = settings.CONTROLS_RIGHT["up"]
            self.down_key = settings.CONTROLS_RIGHT["down"]
        self.y = (settings.SCREEN_HEIGHT - self.height) // 2
        self.rect = pygame.Rect(int(self.x), int(self.y), self.width, self.height)
    def handle_input(self, keys):
        """Move the paddle according to held keys and clamp it to the screen."""
        if keys[self.up_key]:
            self.y -= self.speed
        if keys[self.down_key]:
            self.y += self.speed
        self.y = max(0.0, min(self.y, settings.SCREEN_HEIGHT - self.height))
        self.rect.topleft = (int(self.x), int(self.y))
    def draw(self, surface):
        """Render the paddle with rounded corners."""
        pygame.draw.rect(surface, self.color, self.rect, border_radius=6)