'''
Paddle module.
Defines the Paddle entity controlled by the players. Each paddle moves
vertically, is clamped inside the playfield, and exposes its rectangle
for collision checks with the ball. Rendering is done on a tkinter
Canvas, so no third-party modules are required.
'''
from settings import (
    PADDLE_WIDTH,
    PADDLE_HEIGHT,
    PADDLE_SPEED,
    PADDLE_MARGIN,
    SCREEN_HEIGHT,
)
class Paddle:
    """A vertical paddle controlled by one player."""
    def __init__(self, side, up_key, down_key, color):
        """
        side: 'left' or 'right' — determines the x position.
        up_key / down_key: lowercase tkinter keysyms ('w', 's', 'up', 'down').
        color: hex colour string used when rendering on the canvas.
        """
        self.up_key = up_key
        self.down_key = down_key
        self.color = color
        self.width = PADDLE_WIDTH
        self.height = PADDLE_HEIGHT
        if side == "left":
            self.x = float(PADDLE_MARGIN)
        else:
            self.x = float(SCREEN_WIDTH - PADDLE_MARGIN - PADDLE_WIDTH)
        self.y = float((SCREEN_HEIGHT - PADDLE_HEIGHT) // 2)
        self.speed = PADDLE_SPEED
    def handle_input(self, keys):
        """Move the paddle according to the set of currently held keysyms."""
        if self.up_key in keys:
            self.y -= self.speed
        if self.down_key in keys:
            self.y += self.speed
    def update(self):
        """Clamp the paddle so it never leaves the playfield."""
        if self.y < 0:
            self.y = 0
        if self.y + self.height > SCREEN_HEIGHT:
            self.y = SCREEN_HEIGHT - self.height
    def rect(self):
        """Return the paddle rectangle as (x1, y1, x2, y2)."""
        return (self.x, self.y, self.x + self.width, self.y + self.height)
    def centerx(self):
        """Horizontal centre of the paddle."""
        return self.x + self.width / 2
    def centery(self):
        """Vertical centre of the paddle."""
        return self.y + self.height / 2
    def draw(self, canvas):
        """Render the paddle rectangle on the tkinter canvas."""
        canvas.create_rectangle(
            self.x, self.y, self.x + self.width, self.y + self.height,
            fill=self.color, outline="",
        )