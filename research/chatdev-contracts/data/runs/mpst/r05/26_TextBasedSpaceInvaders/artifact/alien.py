'''alien.py: alien sprites and the fleet that moves them.'''
import random
import pygame
from bullet import Bomb
ROW_COLORS = [(255, 90, 160), (180, 120, 255), (0, 200, 255),
              (80, 255, 120), (255, 220, 90)]
class Alien(pygame.sprite.Sprite):
    """A single alien in the invading fleet."""
    def __init__(self, settings, row, col):
        super().__init__()
        self.settings = settings
        self.row = row
        self.col = col
        # Top rows are worth more points.
        self.points = 10 + (settings.alien_rows - 1 - row) * 5
        self.frames = self._make_frames()
        self.frame_index = 0
        self.image = self.frames[0]
        self.rect = self.image.get_rect()
        self.x = 0.0  # float x position, set precisely by Fleet.create()
    def _make_frames(self):
        """Build two animation frames (legs in/out) drawn with shapes."""
        w, h = self.settings.alien_width, self.settings.alien_height
        color = ROW_COLORS[self.row % len(ROW_COLORS)]
        frames = []
        for leg_offset in (0, 3):
            surf = pygame.Surface((w, h), pygame.SRCALPHA)
            # head/body
            pygame.draw.ellipse(surf, color, (4, 2, w - 8, h - 10))
            # eyes
            pygame.draw.circle(surf, (20, 20, 30), (w // 2 - 7, h // 2 - 2), 3)
            pygame.draw.circle(surf, (20, 20, 30), (w // 2 + 7, h // 2 - 2), 3)
            # legs (offset alternates between frames for a walk cycle)
            pygame.draw.line(surf, color, (8, h - 8), (4 + leg_offset, h - 1), 3)
            pygame.draw.line(surf, color, (w - 8, h - 8), (w - 4 - leg_offset, h - 1), 3)
            frames.append(surf)
        return frames
    def animate(self):
        """Toggle to the other animation frame."""
        self.frame_index = (self.frame_index + 1) % len(self.frames)
        self.image = self.frames[self.frame_index]
class Fleet:
    """Manages the grid of aliens: creation, movement, edge reactions."""
    def __init__(self, settings):
        self.settings = settings
        self.aliens = pygame.sprite.Group()
        self.direction = 1
        self.animation_timer = 0
    def create(self, level=1):
        """(Re)build the fleet; later levels start slightly lower."""
        self.aliens.empty()
        self.direction = 1
        settings = self.settings
        spacing_x = settings.alien_width + 12
        spacing_y = settings.alien_height + 12
        total_w = settings.alien_cols * spacing_x - 12
        start_x = (settings.screen_width - total_w) // 2 + settings.alien_width // 2
        for row in range(settings.alien_rows):
            for col in range(settings.alien_cols):
                alien = Alien(settings, row, col)
                x = start_x + col * spacing_x
                y = settings.fleet_top_margin + row * spacing_y + (level - 1) * 20
                alien.rect.centerx = x
                alien.rect.top = y
                alien.x = float(alien.rect.centerx)
                self.aliens.add(alien)
    def current_speed(self):
        """Fleet speeds up as aliens are destroyed."""
        destroyed = self.settings.alien_rows * self.settings.alien_cols - len(self.aliens)
        return self.settings.alien_base_speed + destroyed * self.settings.alien_speed_increment
    def update(self):
        """Move the fleet sideways; drop and reverse at screen edges."""
        if not self.aliens:
            return
        speed = self.current_speed()
        hit_edge = False
        for alien in self.aliens:
            alien.x += speed * self.direction
            if (alien.x - self.settings.alien_width / 2 <= 0 or
                    alien.x + self.settings.alien_width / 2 >= self.settings.screen_width):
                hit_edge = True
            alien.rect.centerx = int(alien.x)
        if hit_edge:
            self.direction *= -1
            for alien in self.aliens:
                alien.rect.y += self.settings.fleet_drop_speed
                # clamp horizontally
                alien.x = min(max(alien.x, self.settings.alien_width / 2),
                              self.settings.screen_width - self.settings.alien_width / 2)
                alien.rect.centerx = int(alien.x)
        # animate the walk cycle roughly twice per second
        self.animation_timer += 1
        if self.animation_timer >= 30:
            self.animation_timer = 0
            for alien in self.aliens:
                alien.animate()
    def reached_bottom(self, screen_height):
        """True if any alien has descended into the player's zone."""
        limit = screen_height - self.settings.ship_height - 20
        return any(alien.rect.bottom >= limit for alien in self.aliens)
    def maybe_drop_bomb(self, bombs_group):
        """Randomly have an alien drop a bomb (chance per frame, fleet-wide)."""
        if not self.aliens:
            return
        if random.random() < self.settings.bomb_chance:
            self.drop_bomb(bombs_group)
    def drop_bomb(self, bombs_group):
        """Spawn a bomb from the bottom-most alien of a random occupied column."""
        cols = {}
        for alien in self.aliens:
            col = alien.col
            if col not in cols or alien.rect.top > cols[col].rect.top:
                cols[col] = alien
        shooter = random.choice(list(cols.values()))
        bomb = Bomb(self.settings, shooter.rect.centerx, shooter.rect.bottom)
        bombs_group.add(bomb)