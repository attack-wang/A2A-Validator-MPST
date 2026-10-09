'''Game: main game class managing the loop, events, fleet, collisions, and rendering.'''
import sys
import random
import pygame
from settings import Settings
from game_stats import GameStats
from ship import Ship
from alien import Alien
from bullet import Bullet
class Game:
    def __init__(self):
        pygame.init()
        self.settings = Settings()
        self.screen = pygame.display.set_mode(
            (self.settings.screen_width, self.settings.screen_height))
        pygame.display.set_caption(self.settings.caption)
        self.clock = pygame.time.Clock()
        self.stats = GameStats(self.settings)
        self.ship = Ship(self.settings)
        self.aliens = []
        self.player_bullets = []
        self.alien_bullets = []
        self.font = pygame.font.SysFont(None, 28)
        self.big_font = pygame.font.SysFont(None, 64)
        self.fleet_direction = 1
        self.alien_fire_timer = 0
        self.invulnerable_until = 0
    def run(self):
        self._start_new_game()
        while True:
            self._check_events()
            if self.stats.game_active:
                self._update_game()
            self._update_screen()
            self.clock.tick(self.settings.fps)
    def _start_new_game(self):
        self.stats.reset_stats()
        self.ship.reset_position()
        self.player_bullets.clear()
        self.alien_bullets.clear()
        self._create_fleet()
        self.fleet_direction = 1
        self.invulnerable_until = 0
        self.alien_fire_timer = pygame.time.get_ticks()
        self.stats.game_active = True
    def _create_fleet(self):
        self.aliens = []
        for row in range(self.settings.alien_rows):
            for col in range(self.settings.alien_columns):
                alien = Alien(self.settings, row, col)
                alien.place_at(col, row)
                self.aliens.append(alien)
        self.stats.aliens_left = len(self.aliens)
    def _check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)
    def _check_keydown_events(self, event):
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        elif event.key == pygame.K_SPACE and self.stats.game_active:
            self._fire_bullet()
        elif event.key == pygame.K_r and not self.stats.game_active:
            self._start_new_game()
        elif event.key == pygame.K_q:
            pygame.quit()
            sys.exit()
    def _check_keyup_events(self, event):
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False
    def _fire_bullet(self):
        now = pygame.time.get_ticks()
        if self.ship.can_fire(now) and len(self.player_bullets) < self.settings.max_player_bullets:
            self.player_bullets.append(self.ship.fire(now))
    def _update_game(self):
        self.ship.update()
        self._update_bullets()
        self._update_aliens()
        self._alien_fire()
        self._check_collisions()
        self._check_game_end()
    def _update_bullets(self):
        for bullet in self.player_bullets + self.alien_bullets:
            bullet.update()
        self.player_bullets = [b for b in self.player_bullets if not b.is_off_screen()]
        self.alien_bullets = [b for b in self.alien_bullets if not b.is_off_screen()]
    def _update_aliens(self):
        drop = 0
        if self._fleet_hits_edge():
            self.fleet_direction *= -1
            drop = self.settings.fleet_drop_distance
        for alien in self.aliens:
            alien.update(self.fleet_direction, drop)
    def _fleet_hits_edge(self):
        for alien in self.aliens:
            if alien.rect.right >= self.settings.screen_width or alien.rect.left <= 0:
                return True
        return False
    def _alien_fire(self):
        now = pygame.time.get_ticks()
        if now - self.alien_fire_timer >= self.settings.alien_fire_interval_ms and self.aliens:
            self.alien_fire_timer = now
            shooter = random.choice(self.aliens)
            x = shooter.rect.centerx
            y = shooter.rect.bottom
            self.alien_bullets.append(Bullet(self.settings, x, y, 1,
                                             self.settings.alien_bullet_color,
                                             self.settings.alien_bullet_speed))
    def _check_collisions(self):
        '''Handle bullet-alien, bullet-ship, and alien-ship collisions.'''
        now = pygame.time.get_ticks()
        # Player bullets vs aliens
        for bullet in self.player_bullets[:]:
            for alien in self.aliens[:]:
                if bullet.rect.colliderect(alien.rect):
                    self.player_bullets.remove(bullet)
                    self.aliens.remove(alien)
                    self.stats.score += alien.points
                    self.stats.aliens_left -= 1
                    break
        # Alien bullets vs ship (respect invulnerability window)
        if now >= self.invulnerable_until:
            for bullet in self.alien_bullets[:]:
                if bullet.rect.colliderect(self.ship.rect):
                    self.alien_bullets.remove(bullet)
                    self._lose_life(now)
                    break
            # Aliens colliding with the ship also cost a life
            for alien in self.aliens:
                if alien.rect.colliderect(self.ship.rect):
                    self._lose_life(now)
                    break
    def _lose_life(self, now):
        '''Consume one life; end the game if none remain.'''
        self.stats.lives_left -= 1
        if self.stats.lives_left <= 0:
            self.stats.game_active = False
            self.stats.game_won = False
            self.stats.register_game_end()
        else:
            self.invulnerable_until = now + self.settings.invulnerability_ms
            self.ship.reset_position()
            self.alien_bullets.clear()
    def _check_game_end(self):
        # aliens reached bottom (or hit the ship level)
        for alien in self.aliens:
            if alien.rect.bottom >= self.ship.rect.top:
                self.stats.game_active = False
                self.stats.game_won = False
                self.stats.register_game_end()
                return
        if not self.aliens:
            self.stats.game_active = False
            self.stats.game_won = True
            self.stats.register_game_end()
    def _update_screen(self):
        self.screen.fill(self.settings.background_color)
        # HUD
        self._draw_hud()
        if self.stats.game_active:
            self._draw_ship()
            for alien in self.aliens:
                alien.draw(self.screen)
            for bullet in self.player_bullets:
                bullet.draw(self.screen)
            for bullet in self.alien_bullets:
                bullet.draw(self.screen)
        else:
            self._draw_end_screen()
        pygame.display.flip()
    def _draw_ship(self):
        now = pygame.time.get_ticks()
        if now < self.invulnerable_until:
            if (now // 150) % 2 == 0:
                self.ship.draw(self.screen)  # blink
        else:
            self.ship.draw(self.screen)
    def _draw_life_icon(self, x, y):
        points = [(x + 12, y), (x + 24, y + 16), (x, y + 16)]
        pygame.draw.polygon(self.screen, self.settings.ship_color, points)
    def _draw_hud(self):
        score_text = self.font.render(f'Score: {self.stats.score}', True, (255, 255, 255))
        high_text = self.font.render(f'High: {self.stats.high_score}', True, (255, 255, 255))
        aliens_text = self.font.render(f'Aliens: {self.stats.aliens_left}', True, (255, 255, 255))
        self.screen.blit(score_text, (10, 10))
        self.screen.blit(high_text, (10, 40))
        self.screen.blit(aliens_text, (self.settings.screen_width - 150, 10))
        # lives icons
        for i in range(self.stats.lives_left):
            self._draw_life_icon(self.settings.screen_width - 40 - i * 34,
                                 self.settings.screen_height - 30)
    def _draw_end_screen(self):
        if self.stats.game_won is True:
            title = 'VICTORY!'
            color = (80, 220, 120)
        else:
            title = 'GAME OVER'
            color = (255, 70, 70)
        title_surf = self.big_font.render(title, True, color)
        title_rect = title_surf.get_rect(center=(self.settings.screen_width // 2,
                                                 self.settings.screen_height // 2 - 40))
        self.screen.blit(title_surf, title_rect)
        score_surf = self.font.render(f'Final score: {self.stats.score}  (High: {self.stats.high_score})',
                                      True, (255, 255, 255))
        score_rect = score_surf.get_rect(center=(self.settings.screen_width // 2,
                                                 self.settings.screen_height // 2 + 20))
        self.screen.blit(score_surf, score_rect)
        prompt_surf = self.font.render('Press R to restart, Q to quit', True, (200, 200, 200))
        prompt_rect = prompt_surf.get_rect(center=(self.settings.screen_width // 2,
                                                   self.settings.screen_height // 2 + 60))
        self.screen.blit(prompt_surf, prompt_rect)