'''
sprites.py
Sprite classes for the Space Invaders game:
Player (the ship), Alien, Bullet (player shot) and Bomb (alien shot).
All graphics are generated procedurally with pygame surfaces so the
game runs without external image assets.
'''
import pygame
import settings
class Player(pygame.sprite.Sprite):
    """Player's ship. Moves horizontally along the bottom of the screen."""
    def __init__(self):
        super().__init__()
        self.image = self._make_image()
        self.rect = self.image.get_rect(
            midbottom=(settings.PLAYER_START_X, settings.PLAYER_START_Y)
        )
        self.last_shot = 0  # timestamp (ms) of the last shot fired
    @staticmethod
    def _make_image():
        """Draw a simple triangular ship on a transparent surface."""
        surf = pygame.Surface((settings.PLAYER_WIDTH, settings.PLAYER_HEIGHT), pygame.SRCALPHA)
        pygame.draw.polygon(surf, settings.CYAN, [
            (settings.PLAYER_WIDTH // 2, 0),
            (settings.PLAYER_WIDTH, settings.PLAYER_HEIGHT),
            (0, settings.PLAYER_HEIGHT),
        ])
        pygame.draw.rect(surf, settings.WHITE,
                         (settings.PLAYER_WIDTH // 2 - 3, settings.PLAYER_HEIGHT - 10, 6, 10))
        return surf
    def update(self, dt=1):
        """Move the ship according to currently pressed keys."""
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.rect.x -= settings.PLAYER_SPEED
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.rect.x += settings.PLAYER_SPEED
        # Keep the ship inside the screen bounds
        self.rect.clamp_ip(pygame.Rect(0, 0, settings.WIDTH, settings.HEIGHT))
    def can_shoot(self):
        """True when the firing cooldown has elapsed."""
        return pygame.time.get_ticks() - self.last_shot >= settings.PLAYER_COOLDOWN
    def shoot(self):
        """Return a fresh Bullet if the cooldown allows it, otherwise None."""
        if self.can_shoot():
            self.last_shot = pygame.time.get_ticks()
            return Bullet(self.rect.centerx, self.rect.top)
        return None
class Alien(pygame.sprite.Sprite):
    """A single alien. Movement is controlled by the Fleet object."""
    def __init__(self, row, col, x, y):
        super().__init__()
        self.row = row
        self.col = col
        # Top rows are worth more points; clamp index for safety
        self.points = settings.ALIEN_POINTS[min(row, len(settings.ALIEN_POINTS) - 1)]
        self.image = self._make_image(row)
        self.rect = self.image.get_rect(topleft=(x, y))
    @staticmethod
    def _make_image(row):
        """Draw a colored alien body with eyes and legs, one color per row."""
        colors = [settings.RED, settings.ORANGE, settings.YELLOW, settings.GREEN, settings.CYAN]
        color = colors[row % len(colors)]
        w, h = settings.ALIEN_WIDTH, settings.ALIEN_HEIGHT
        surf = pygame.Surface((w, h), pygame.SRCALPHA)
        # body
        pygame.draw.ellipse(surf, color, (2, 4, w - 4, h - 10))
        # eyes
        pygame.draw.circle(surf, settings.BLACK, (w // 2 - 7, h // 2), 3)
        pygame.draw.circle(surf, settings.BLACK, (w // 2 + 7, h // 2), 3)
        # legs / antennae
        pygame.draw.line(surf, color, (6, h - 6), (2, h - 1), 2)
        pygame.draw.line(surf, color, (w - 6, h - 6), (w - 2, h - 1), 2)
        return surf
class Bullet(pygame.sprite.Sprite):
    """Shot fired by the player; travels upwards and dies off-screen."""
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((settings.BULLET_WIDTH, settings.BULLET_HEIGHT), pygame.SRCALPHA)
        self.image.fill(settings.BULLET_COLOR)
        self.rect = self.image.get_rect(center=(x, y))
    def update(self, dt=1):
        """Move upwards (BULLET_SPEED is negative) and die above the screen."""
        self.rect.y += settings.BULLET_SPEED
        if self.rect.bottom < 0:
            self.kill()
class Bomb(pygame.sprite.Sprite):
    """Bomb dropped by aliens; travels downwards and dies off-screen."""
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((settings.BOMB_WIDTH, settings.BOMB_HEIGHT), pygame.SRCALPHA)
        self.image.fill(settings.BOMB_COLOR)
        self.rect = self.image.get_rect(center=(x, y))
    def update(self, dt=1):
        """Move downwards and die below the screen."""
        self.rect.y += settings.BOMB_SPEED
        if self.rect.top > settings.HEIGHT:
            self.kill()