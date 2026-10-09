'''
ship.py
The player-controlled ship: horizontal movement, firing with a cooldown,
lives and brief invincibility after being hit. Drawn with tkinter
canvas primitives (a polygon hull plus a cockpit dot).
'''
from settings import Settings
class Ship:
    """The player's ship at the bottom of the screen."""
    def __init__(self, game):
        self.game = game
        self.lives = Settings.SHIP_START_LIVES
        self.cooldown = 0.0
        self.invincible_timer = 0.0
        self.blink_timer = 0.0
        self.width = Settings.SHIP_WIDTH
        self.height = Settings.SHIP_HEIGHT
        self.reset_position()
    def reset_position(self):
        """Center the ship horizontally near the bottom of the screen."""
        self.x = float(Settings.SCREEN_WIDTH // 2 - self.width // 2)
        self.y = float(Settings.SCREEN_HEIGHT - 24 - self.height)
    @property
    def rect(self):
        return (self.x, self.y, self.x + self.width, self.y + self.height)
    @property
    def centerx(self):
        return self.x + self.width / 2.0
    @property
    def top(self):
        return self.y
    def update(self, dt, keys):
        """Move the ship according to held keys and tick down timers."""
        move = 0.0
        if "Left" in keys or "a" in keys or "A" in keys:
            move -= 1.0
        if "Right" in keys or "d" in keys or "D" in keys:
            move += 1.0
        self.x += move * Settings.SHIP_SPEED * dt
        if self.x < Settings.SHIP_MARGIN:
            self.x = Settings.SHIP_MARGIN
        if self.x + self.width > Settings.SCREEN_WIDTH - Settings.SHIP_MARGIN:
            self.x = Settings.SCREEN_WIDTH - Settings.SHIP_MARGIN - self.width
        self.cooldown = max(0.0, self.cooldown - dt)
        if self.invincible_timer > 0.0:
            self.invincible_timer = max(0.0, self.invincible_timer - dt)
            self.blink_timer += dt
    def try_fire(self):
        """Fire a bullet if the cooldown has expired and slots are free."""
        if self.cooldown > 0.0:
            return
        if len(self.game.player_bullets) >= Settings.MAX_PLAYER_BULLETS:
            return
        self.game.player_bullets.append(
            Bullet(self.centerx, self.top, Settings.PLAYER_BULLET_SPEED,
                   Settings.PLAYER_BULLET_COLOR, -1, "player"))
        self.cooldown = Settings.SHIP_FIRE_COOLDOWN
    def hit(self):
        """The ship was struck: lose a life, respawn, gain invincibility."""
        self.lives -= 1
        self.invincible_timer = Settings.INVINCIBILITY_TIME
        self.reset_position()
    @property
    def is_invincible(self):
        return self.invincible_timer > 0.0
    def draw(self, canvas):
        """Draw the ship (blinking while invincible)."""
        if self.is_invincible and int(self.blink_timer * 10) % 2 == 0:
            return
        x, y = int(self.x), int(self.y)
        w, h = self.width, self.height
        color = Settings.SHIP_COLOR
        canvas.create_polygon(
            x + w // 2, y,
            x + 3 * w // 4, y + 2 * h // 3,
            x + w, y + h,
            x, y + h,
            x + w // 4, y + 2 * h // 3,
            fill=color, outline="")
        canvas.create_oval(x + w // 2 - 3, y + h // 2 - 3,
                           x + w // 2 + 3, y + h // 2 + 3,
                           fill="#ffffff", outline="")