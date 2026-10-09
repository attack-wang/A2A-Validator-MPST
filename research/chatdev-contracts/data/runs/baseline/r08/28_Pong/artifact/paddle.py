'''
Paddle entity: a vertical bar a player moves up and down with two keys.
'''
import pygame
import settings
class Paddle:
    '''A player-controlled vertical paddle that stays inside the playfield.'''
    def __init__(self, side, up_key, down_key):
        '''Build a paddle on `side` ("left" or "right") bound to two keys.'''
        self.up_key = up_key
        self.down_key = down_key
        self.speed = settings.PADDLE_SPEED
        if side == "left":
            x = settings.PADDLE_MARGIN
            self.color = settings.COLOR_PADDLE_LEFT
        elif side == "right":
            x = settings.SCREEN_WIDTH - settings.PADDLE_MARGIN - settings.PADDLE_WIDTH
            self.color = settings.COLOR_PADDLE_RIGHT
        else:
            raise ValueError("side must be 'left' or 'right'")
        self.y = float((settings.SCREEN_HEIGHT - settings.PADDLE_HEIGHT) // 2)
        self.rect = pygame.Rect(x, int(self.y), settings.PADDLE_WIDTH, settings.PADDLE_HEIGHT)
    def update(self, dt, keys):
        '''Move the paddle from held keys and clamp it to the screen.'''
        direction = 0.0
        if keys[self.up_key]:
            direction -= 1.0
        if keys[self.down_key]:
            direction += 1.0
        self.y += direction * self.speed * dt
        top_limit = 0.0
        bottom_limit = float(settings.SCREEN_HEIGHT - settings.PADDLE_HEIGHT)
        if self.y < top_limit:
            self.y = top_limit
        elif self.y > bottom_limit:
            self.y = bottom_limit
        self.rect.y = int(round(self.y))
    def draw(self, surface):
        '''Render the paddle with slightly rounded corners.'''
        pygame.draw.rect(surface, self.color, self.rect, border_radius=4)