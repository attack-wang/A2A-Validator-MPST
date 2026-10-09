'''
alien_fleet.py
Manages the alien grid: marching movement with descent, speed-up as
aliens die, two-frame animation, and bottom-most-alien firing.
'''
import random
from settings import Settings
from alien import Alien
from bullet import Bullet
class AlienFleet:
    """The grid of invaders: movement, descent, animation and firing."""
    def __init__(self, game, wave):
        self.game = game
        self.wave = wave
        self.aliens = []
        self.direction = 1
        self.speed = Settings.ALIEN_BASE_SPEED + (wave - 1) * Settings.ALIEN_WAVE_SPEED_BONUS
        self.fire_timer = random.uniform(Settings.ALIEN_FIRE_MIN, Settings.ALIEN_FIRE_MAX)
        self.animation_timer = 0.0
        self.animation_frame = 0
        self.create_fleet()
    def create_fleet(self):
        """Build a centered grid of aliens for this wave."""
        self.aliens.clear()
        cols = Settings.ALIEN_COLS
        rows = Settings.ALIEN_ROWS
        step_x = Settings.ALIEN_WIDTH + Settings.ALIEN_X_SPACING
        step_y = Settings.ALIEN_HEIGHT + Settings.ALIEN_Y_SPACING
        total_width = cols * step_x - Settings.ALIEN_X_SPACING
        start_x = (Settings.SCREEN_WIDTH - total_width) // 2
        start_y = Settings.FLEET_TOP_OFFSET
        for row in range(rows):
            for col in range(cols):
                x = start_x + col * step_x
                y = start_y + row * step_y
                self.aliens.append(Alien(self.game, row, col, x, y))
    @property
    def alive_aliens(self):
        return [a for a in self.aliens if a.alive]
    @property
    def alive_count(self):
        return sum(1 for a in self.aliens if a.alive)
    @property
    def all_destroyed(self):
        return self.alive_count == 0
    def update(self, dt):
        """March the fleet, animate it, and let aliens fire."""
        alive = self.alive_aliens
        if not alive:
            return
        total = max(1, len(self.aliens))
        ratio = len(alive) / total
        speed = self.speed
        if ratio <= 0.25:
            speed *= Settings.ALIEN_RUSH_FACTOR
        elif ratio <= 0.5:
            speed *= 1.5
        dx = self.direction * speed * dt
        dy = 0.0
        edge_reached = False
        for alien in alive:
            if self.direction > 0 and alien.x + alien.width + dx >= Settings.SCREEN_WIDTH - Settings.FLEET_SIDE_MARGIN:
                edge_reached = True
                break
            if self.direction < 0 and alien.x + dx <= Settings.FLEET_SIDE_MARGIN:
                edge_reached = True
                break
        if edge_reached:
            self.direction *= -1
            dy = Settings.ALIEN_DESCENT_STEP
            dx = self.direction * speed * dt
        for alien in alive:
            alien.update_position(dx, dy)
        self.animation_timer += dt
        if self.animation_timer >= 0.35:
            self.animation_timer = 0.0
            self.animation_frame = 1 - self.animation_frame
            for alien in alive:
                alien.set_animation_frame(self.animation_frame)
        self.fire_timer -= dt
        if self.fire_timer <= 0.0:
            max_gap = max(Settings.ALIEN_FIRE_MIN,
                          Settings.ALIEN_FIRE_MAX * (Settings.ALIEN_FIRE_WAVE_SCALE ** (self.wave - 1)))
            self.fire_timer = random.uniform(Settings.ALIEN_FIRE_MIN, max_gap)
            self._alien_fire(alive)
    def _alien_fire(self, alive):
        """Pick a random column's bottom-most alien and drop a bullet."""
        bottom_most = {}
        for alien in alive:
            col = alien.col
            if col not in bottom_most or alien.y > bottom_most[col].y:
                bottom_most[col] = alien
        shooter = random.choice(list(bottom_most.values()))
        self.game.alien_bullets.append(
            Bullet(shooter.x + shooter.width / 2.0, shooter.y + shooter.height,
                   Settings.ALIEN_BULLET_SPEED, Settings.ALIEN_BULLET_COLOR, 1, "alien"))
    def check_bottom(self, threshold_y):
        """True if any living alien has reached the invasion line."""
        return any(a.alive and a.y + a.height >= threshold_y for a in self.aliens)
    def draw(self, canvas):
        for alien in self.aliens:
            alien.draw(canvas)