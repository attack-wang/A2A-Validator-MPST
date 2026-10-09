"""Alien and AlienFleet: the descending grid of invaders."""
import random
import settings
ALIEN_PATTERN = [
    "..X.....X..",
    "...X...X...",
    "..XXXXXXX..",
    ".XX.XXX.XX.",
    "XXXXXXXXXXX",
    "X.XXXXXXX.X",
    "X.X.....X.X",
    "...XX.XX...",
]
ALIEN_WIDTH = len(ALIEN_PATTERN[0]) * 3   # 33
ALIEN_HEIGHT = len(ALIEN_PATTERN) * 3     # 24
class Alien:
    def __init__(self, x, y, points):
        self.x = float(x)
        self.y = float(y)
        self.width = ALIEN_WIDTH
        self.height = ALIEN_HEIGHT
        self.points = points
        self.alive = True
    @property
    def rect(self):
        return (self.x, self.y, self.x + self.width, self.y + self.height)
    @property
    def centerx(self):
        return self.x + self.width / 2.0
    @property
    def bottom(self):
        return self.y + self.height
class AlienFleet:
    def __init__(self):
        self.aliens = []
        self.direction = 1
        self.speed = settings.ALIEN_BASE_SPEED
        self.bomb_timer = 0.0
        self._build()
    def _build(self):
        for row in range(settings.ALIEN_ROWS):
            if row == 0:
                points = settings.ALIEN_POINTS_TOP
            elif row <= 2:
                points = settings.ALIEN_POINTS_MIDDLE
            else:
                points = settings.ALIEN_POINTS_BOTTOM
            for col in range(settings.ALIEN_COLS):
                x = settings.ALIEN_HORIZONTAL_PADDING + col * settings.ALIEN_SPACING_X
                y = settings.ALIEN_TOP_OFFSET + row * settings.ALIEN_SPACING_Y
                self.aliens.append(Alien(x, y, points))
    @property
    def alive_aliens(self):
        return [a for a in self.aliens if a.alive]
    def remaining(self):
        return len(self.alive_aliens)
    def total(self):
        return len(self.aliens)
    def update(self, dt):
        """Move the fleet; returns a new AlienBomb or None."""
        if not self.alive_aliens:
            return None
        destroyed_fraction = 1 - self.remaining() / self.total()
        self.speed = settings.ALIEN_BASE_SPEED + (settings.ALIEN_MAX_SPEED - settings.ALIEN_BASE_SPEED) * destroyed_fraction
        move_x = self.direction * self.speed * dt
        leftmost = min(a.x for a in self.alive_aliens)
        rightmost = max(a.x + a.width for a in self.alive_aliens)
        if (self.direction > 0 and rightmost + move_x >= settings.SCREEN_WIDTH - 10) or \
           (self.direction < 0 and leftmost + move_x <= 10):
            self.direction *= -1
            for alien in self.alive_aliens:
                alien.y += settings.ALIEN_DROP_DISTANCE
        else:
            for alien in self.alive_aliens:
                alien.x += move_x
        return self.maybe_drop_bomb(dt)
    def maybe_drop_bomb(self, dt):
        if not self.alive_aliens:
            return None
        self.bomb_timer = max(0.0, self.bomb_timer - dt)
        if self.bomb_timer > 0:
            return None
        # expected ALIEN_BOMB_CHANCE bombs per second
        if random.random() < settings.ALIEN_BOMB_CHANCE * dt:
            shooter = random.choice(self.alive_aliens)
            self.bomb_timer = settings.ALIEN_BOMB_COOLDOWN
            return AlienBomb(shooter.centerx, shooter.bottom)
        return None
    def reached_bottom(self):
        limit_y = settings.SCREEN_HEIGHT - settings.ALIEN_BOTTOM_LIMIT
        return any(a.bottom >= limit_y for a in self.alive_aliens)