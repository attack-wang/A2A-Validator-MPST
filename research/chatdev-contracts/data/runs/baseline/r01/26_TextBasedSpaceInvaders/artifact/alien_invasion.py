'''
alien_invasion.py
Main game class: manages the game loop, events, fleet, collisions, and rendering.
'''
import random
import sys
import pygame
import settings
from ship import Ship
from alien import Alien
from bullet import Bullet
from game_stats import GameStats
from scoreboard import Scoreboard
class AlienInvasion:
    """Overall class to manage game assets and behavior."""
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT))
        pygame.display.set_caption(settings.SCREEN_TITLE)
        self.clock = pygame.time.Clock()
        self.stats = GameStats()
        self.scoreboard = Scoreboard(self.screen, self.stats)
        self.ship = Ship(self.screen)
        self.player_bullets = []
        self.alien_bombs = []
        self.aliens = []
        self.fleet_direction = 1
        self.last_shot_time = 0
        self._create_fleet()
    def run_game(self):
        """Main game loop."""
        self.stats.game_active = True
        while True:
            self._check_events()
            if self.stats.game_active:
                self.ship.update()
                self._update_player_bullets()
                self._update_aliens()
                self._alien_fire()
                self._update_alien_bombs()
            self._update_screen()
            self.clock.tick(settings.FPS)
    # ------------------------- Event handling -------------------------
    def _check_events(self):
        """Respond to keyboard and window events."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)
    def _check_keydown_events(self, event):
        """Handle key presses: movement, firing, quit, restart."""
        if event.key in (pygame.K_RIGHT, pygame.K_d):
            self.ship.moving_right = True
        elif event.key in (pygame.K_LEFT, pygame.K_a):
            self.ship.moving_left = True
        elif event.key == pygame.K_SPACE and self.stats.game_active:
            self._fire_bullet()
        elif event.key == pygame.K_q:
            pygame.quit()
            sys.exit()
        elif event.key == pygame.K_r and not self.stats.game_active:
            self._restart_game()
    def _check_keyup_events(self, event):
        """Handle key releases: stop movement."""
        if event.key in (pygame.K_RIGHT, pygame.K_d):
            self.ship.moving_right = False
        elif event.key in (pygame.K_LEFT, pygame.K_a):
            self.ship.moving_left = False
    # ------------------------- Player firing --------------------------
    def _fire_bullet(self):
        """Fire a bullet if the cooldown has elapsed."""
        now = pygame.time.get_ticks()
        if now - self.last_shot_time >= settings.BULLET_COOLDOWN:
            self.last_shot_time = now
            self.player_bullets.append(
                Bullet(self.screen, self.ship.rect.centerx, self.ship.rect.top, 1))
    def _update_player_bullets(self):
        """Move bullets, remove off-screen ones, check alien hits."""
        for bullet in self.player_bullets[:]:
            bullet.update()
            if bullet.is_off_screen():
                self.player_bullets.remove(bullet)
        self._check_bullet_alien_collisions()
    def _check_bullet_alien_collisions(self):
        """Destroy hit aliens, add score, end game with victory when fleet is cleared."""
        for bullet in self.player_bullets[:]:
            for alien in self.aliens[:]:
                if bullet.rect.colliderect(alien.rect):
                    self.player_bullets.remove(bullet)
                    self.aliens.remove(alien)
                    self.stats.score += settings.POINTS_PER_ALIEN
                    if self.stats.score > self.stats.high_score:
                        self.stats.high_score = self.stats.score
                    break
        if not self.aliens and self.stats.game_active:
            self.stats.game_active = False
            self.stats.victory = True
    # ------------------------- Fleet management -----------------------
    def _create_fleet(self):
        """Create a centered grid of aliens near the top of the screen."""
        alien = Alien(self.screen, 0, 0)
        aw, ah = alien.rect.width, alien.rect.height
        spacing_x, spacing_y = 12, 12
        fleet_width = settings.ALIEN_COLUMNS * aw + (settings.ALIEN_COLUMNS - 1) * spacing_x
        start_x = (settings.SCREEN_WIDTH - fleet_width) // 2
        for row in range(settings.ALIEN_ROWS):
            for col in range(settings.ALIEN_COLUMNS):
                alien = Alien(self.screen, row, col)
                alien.set_position(start_x + col * (aw + spacing_x),
                                   60 + row * (ah + spacing_y))
                self.aliens.append(alien)
    def _update_aliens(self):
        """Move fleet sideways, drop & reverse at edges, check bottom/ship contact."""
        if not self.aliens:
            return
        screen_rect = self.screen.get_rect()
        if any(alien.check_edges(screen_rect) for alien in self.aliens):
            for alien in self.aliens:
                alien.drop()
            self.fleet_direction *= -1
        else:
            for alien in self.aliens:
                alien.update(self.fleet_direction)
        if self._aliens_reached_bottom():
            self.stats.game_active = False
            self.stats.game_over = True
            self.stats.victory = False
            return
        # An alien touching the ship costs a life; remove that alien to avoid repeat hits
        for alien in self.aliens[:]:
            if alien.rect.colliderect(self.ship.rect):
                self.aliens.remove(alien)
                self._ship_hit()
                break
    def _aliens_reached_bottom(self):
        """Return True if any alien has descended to the ship's level."""
        screen_rect = self.screen.get_rect()
        return any(alien.rect.bottom >= screen_rect.bottom - 10 for alien in self.aliens)
    def _ship_hit(self):
        """Handle the ship being hit: lose a life, or end the game at zero lives."""
        self.stats.lives -= 1
        self.alien_bombs.clear()
        self.player_bullets.clear()
        if self.stats.lives > 0:
            self.ship.center_ship()
        else:
            self.stats.game_active = False
            self.stats.game_over = True
            self.stats.victory = False
    # ------------------------- Alien bombs ----------------------------
    def _alien_fire(self):
        """Randomly drop a bomb from the lowest alien of a random column."""
        if not self.aliens or random.random() >= settings.ALIEN_FIRE_CHANCE:
            return
        cols = {}
        for alien in self.aliens:
            if alien.col not in cols or alien.rect.top > cols[alien.col].rect.top:
                cols[alien.col] = alien
        shooter = random.choice(list(cols.values()))
        self.alien_bombs.append(
            Bullet(self.screen, shooter.rect.centerx, shooter.rect.bottom, -1))
    def _update_alien_bombs(self):
        """Move bombs, remove off-screen ones, check hits on the ship."""
        for bomb in self.alien_bombs[:]:
            bomb.update()
            if bomb.is_off_screen():
                self.alien_bombs.remove(bomb)
            elif bomb.rect.colliderect(self.ship.rect):
                self.alien_bombs.remove(bomb)
                self._ship_hit()
    # ------------------------- Restart / rendering --------------------
    def _restart_game(self):
        """Reset stats and rebuild the fleet for a new game."""
        self.stats.reset_stats()
        self.stats.game_active = True
        self.stats.game_over = False
        self.stats.victory = False
        self.player_bullets.clear()
        self.alien_bombs.clear()
        self.aliens.clear()
        self.ship.center_ship()
        self.fleet_direction = 1
        self.last_shot_time = 0
        self._create_fleet()
    def _update_screen(self):
        """Redraw background, all objects, HUD, and end-game messages."""
        self.screen.fill(settings.BG_COLOR)
        for bullet in self.player_bullets:
            bullet.blitme()
        for bomb in self.alien_bombs:
            bomb.blitme()
        for alien in self.aliens:
            alien.blitme()
        self.ship.blitme()
        self.scoreboard.show_score()
        if self.stats.game_over:
            self.scoreboard.draw_center_message("GAME OVER", "Press R to restart, Q to quit")
        elif self.stats.victory:
            self.scoreboard.draw_center_message("VICTORY!", "All aliens defeated - Press R to restart")
        pygame.display.flip()