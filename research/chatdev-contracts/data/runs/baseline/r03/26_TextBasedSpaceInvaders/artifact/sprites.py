'''
sprites.py
Sprite classes for the simplified Space Invaders game:
- Player: the ship controlled by the player (horizontal movement, shooting,
  lives and brief invulnerability after being hit).
- Alien: one member of the invading grid; knows its row/column and point
  value and moves horizontally with the rest of the formation.
- Bullet: a projectile fired either by the player (upward) or by an alien
  (downward); destroys itself when it leaves the screen.
'''
import pygame
import settings
class Player(pygame.sprite.Sprite):
    '''Player-controlled ship at the bottom of the screen.'''
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((settings.PLAYER_WIDTH, settings.PLAYER_HEIGHT))
        self.image.fill(settings.PLAYER_COLOR)
        # Small cannon on top of the hull
        pygame.draw.rect(
            self.image,
            settings.WHITE,
            (settings.PLAYER_WIDTH // 2 - 4, 0, 8, 12),
        )
        self.rect = self.image.get_rect(
            midbottom=(settings.SCREEN_WIDTH // 2,
                       settings.SCREEN_HEIGHT - settings.PLAYER_Y_OFFSET)
        )
        self.speed = settings.PLAYER_SPEED
        self.lives = settings.PLAYER_START_LIVES
        self.shoot_cooldown_until = 0
        self.invulnerable_until = 0
    def update(self):
        '''Handle horizontal movement and invulnerability blinking.'''
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.rect.x += self.speed
        # Keep the ship inside the screen bounds
        self.rect.left = max(self.rect.left, 0)
        self.rect.right = min(self.rect.right, settings.SCREEN_WIDTH)
        # Blink while invulnerable right after being hit
        now = pygame.time.get_ticks()
        if now < self.invulnerable_until:
            self.image.set_alpha(90 if (now // 100) % 2 == 0 else 255)
        else:
            self.image.set_alpha(255)
    def shoot(self, now_ms):
        '''Return a fresh player Bullet if the cooldown allows, else None.'''
        if now_ms < self.shoot_cooldown_until:
            return None
        self.shoot_cooldown_until = now_ms + settings.PLAYER_SHOOT_COOLDOWN_MS
        return Bullet(
            self.rect.centerx,
            self.rect.top,
            settings.PLAYER_BULLET_SPEED,
            settings.PLAYER_BULLET_COLOR,
        )
    def hit(self, now_ms):
        '''Register a hit. Returns True if a life was actually lost.'''
        if now_ms < self.invulnerable_until:
            return False  # still invulnerable: ignore the hit
        self.lives -= 1
        self.invulnerable_until = now_ms + settings.PLAYER_RESPAWN_INVULNERABILITY_MS
        # Respawn at the starting position
        self.rect.midbottom = (settings.SCREEN_WIDTH // 2,
                               settings.SCREEN_HEIGHT - settings.PLAYER_Y_OFFSET)
        return True
class Alien(pygame.sprite.Sprite):
    '''A single alien belonging to the invading formation.'''
    def __init__(self, row, col):
        super().__init__()
        self.row = row
        self.col = col
        # Top rows are worth more points
        self.score_value = settings.ALIEN_BASE_SCORE * (settings.ALIEN_ROWS - row)
        color = settings.ALIEN_COLORS[row % len(settings.ALIEN_COLORS)]
        self.image = pygame.Surface((settings.ALIEN_WIDTH, settings.ALIEN_HEIGHT))
        self.image.fill(color)
        # Simple "face": two dark eyes and a mouth line
        pygame.draw.rect(self.image, settings.BLACK, (7, 9, 7, 7))
        pygame.draw.rect(self.image, settings.BLACK,
                         (settings.ALIEN_WIDTH - 14, 9, 7, 7))
        pygame.draw.rect(self.image, settings.BLACK,
                         (10, settings.ALIEN_HEIGHT - 8, settings.ALIEN_WIDTH - 20, 3))
        x = settings.ALIEN_GRID_START_X + col * settings.ALIEN_SPACING_X
        y = settings.ALIEN_TOP_MARGIN + row * settings.ALIEN_SPACING_Y
        self.rect = self.image.get_rect(topleft=(x, y))
    def update(self, direction):
        '''Move horizontally in the current formation direction.'''
        self.rect.x += direction * settings.ALIEN_HORIZONTAL_SPEED
class Bullet(pygame.sprite.Sprite):
    '''A projectile fired by the player (upward) or by an alien (downward).'''
    def __init__(self, x, y, speed, color):
        super().__init__()
        self.image = pygame.Surface((settings.BULLET_WIDTH, settings.BULLET_HEIGHT))
        self.image.fill(color)
        self.rect = self.image.get_rect(center=(x, y))
        self.speed = speed
    def update(self):
        '''Move the bullet and remove it once it leaves the screen.'''
        self.rect.y += self.speed
        if self.rect.bottom < 0 or self.rect.top > settings.SCREEN_HEIGHT:
            self.kill()