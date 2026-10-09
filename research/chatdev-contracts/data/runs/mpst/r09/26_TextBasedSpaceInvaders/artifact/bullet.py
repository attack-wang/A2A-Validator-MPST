"""Projectile classes: player bullets and alien bombs."""
import settings
class Bullet:
    """A simple vertical projectile fired either by the player or an alien."""
    def __init__(self, x, y, speed, color, width, height):
        self.x = float(x)
        self.y = float(y)
        self.speed = speed
        self.color = color
        self.width = width
        self.height = height
        self.dead = False
    def update(self, dt):
        """Move the bullet vertically; negative speed moves upward."""
        self.y += self.speed * dt
        if self.off_screen:
            self.dead = True
    @property
    def rect(self):
        left = self.x - self.width / 2.0
        return (left, self.y, left + self.width, self.y + self.height)
    @property
    def off_screen(self):
        return self.y + self.height < 0 or self.y > settings.SCREEN_HEIGHT
    @staticmethod
    def rects_overlap(a, b):
        return not (a[2] < b[0] or b[2] < a[0] or a[3] < b[1] or b[3] < a[1])
    def hits(self, other_rect):
        return self.rects_overlap(self.rect, other_rect)
class PlayerBullet(Bullet):
    def __init__(self, x, y):
        super().__init__(x, y, -settings.PLAYER_BULLET_SPEED,
                         settings.COLOR_YELLOW,
                         settings.PLAYER_BULLET_WIDTH, settings.PLAYER_BULLET_HEIGHT)
class AlienBomb(Bullet):
    def __init__(self, x, y):
        super().__init__(x, y, settings.ALIEN_BOMB_SPEED,
                         settings.COLOR_RED,
                         settings.ALIEN_BOMB_WIDTH, settings.ALIEN_BOMB_HEIGHT)