'''
bullet.py
Defines the Bullet class used for both player and alien projectiles.
Bullets travel in a straight vertical line and deactivate when they
leave the screen. Positions are plain floats; drawing happens in the
game's render pass.
'''
from settings import Settings
class Bullet:
    """A single projectile fired either by the player or by an alien."""
    def __init__(self, x, y, speed, color, direction, owner):
        """
        Create a bullet.
        x, y      : starting centre-x and top/bottom-y (pixels)
        speed     : vertical speed in pixels per second (positive value)
        color     : colour string used when drawing
        direction : +1 for downward (alien), -1 for upward (player)
        owner     : "player" or "alien" - used for collision filtering
        """
        self.owner = owner
        self.color = color
        self.speed = speed * direction
        self.x = float(x)  # centre x
        self.y = float(y)  # reference y (nose of ship / bottom of alien)
        self.active = True
    @property
    def rect(self):
        """Current bounding box (x0, y0, x1, y1)."""
        x0 = self.x - Settings.BULLET_WIDTH / 2.0
        if self.speed < 0:  # moving up: y is the bottom edge
            y1 = self.y
            y0 = y1 - Settings.BULLET_HEIGHT
        else:               # moving down: y is the top edge
            y0 = self.y
            y1 = y0 + Settings.BULLET_HEIGHT
        return (x0, y0, x0 + Settings.BULLET_WIDTH, y1)
    def update(self, dt):
        """Move the bullet and deactivate it once it leaves the screen."""
        self.y += self.speed * dt
        r = self.rect
        if r[3] < 0 or r[1] > Settings.SCREEN_HEIGHT:
            self.active = False
    def draw(self, canvas):
        """Render the bullet as a small rectangle with a bright core."""
        x0, y0, x1, y1 = self.rect
        canvas.create_rectangle(x0, y0, x1, y1, fill=self.color, outline="")
        canvas.create_rectangle(x0 + 1, y0 + 5, x1 - 1, y1 - 5,
                                fill="#ffffff", outline="")