'''
game.py: core game object — main loop, state machine, collisions and rendering.
'''
import sys
import pygame
from settings import Settings
from game_stats import GameStats
from ship import Ship
from fleet import Fleet
from scoreboard import Scoreboard
from explosion import Explosion
class Game:
    """Overall class to manage game behavior, assets and the state machine."""
    def __init__(self):
        pygame.init()
        self.settings = Settings()
        self.screen = pygame.display.set_mode(
            (self.settings.screen_width, self.settings.screen_height))
        pygame.display.set_caption(self.settings.caption)
        self.clock = pygame.time.Clock()
        self.stats = GameStats(self.settings)
        self.scoreboard = Scoreboard(self)
        self.bullets = []
        self.effects = []
        self.ship = Ship(self)
        self.fleet = None
        self.flash_timer = 0.0
        self.wave_clear_timer = 0.0
        self.big_font = pygame.font.SysFont(None, 64)
        self.small_font = pygame.font.SysFont(None, 30)
        self.state = 'start'  # start -> playing -> wave_clear -> game_over
    def run(self):
        """Main game loop (delta-time based)."""
        while True:
            dt = self.clock.tick(self.settings.fps) / 1000.0
            self._check_events()
            self._update(dt)
            self._update_screen()
    # ------------------------------------------------------------- events
    def _check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                elif event.key == pygame.K_SPACE and self.state in ('start', 'game_over'):
                    self._start_game()
                elif event.key == pygame.K_p:
                    if self.state == 'playing':
                        self.state = 'paused'
                    elif self.state == 'paused':
                        self.state = 'playing'
    def _handle_continuous_fire(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            bullet = self.ship.fire()
            if bullet:
                self.bullets.append(bullet)
    # ------------------------------------------------------------- update
    def _update(self, dt):
        self.flash_timer = max(0.0, self.flash_timer - dt)
        self._update_effects(dt)
        if self.state == 'playing':
            self._handle_continuous_fire()
            self.ship.update(dt)
            self.fleet.update(dt)
            self._update_bullets(dt)
            self._check_collisions()
            self._check_game_conditions()
        elif self.state == 'wave_clear':
            self.wave_clear_timer -= dt
            if self.wave_clear_timer <= 0:
                self.stats.level += 1
                self._spawn_fleet()
                self.state = 'playing'
    def _update_bullets(self, dt):
        for bullet in self.bullets:
            bullet.update(dt)
        self.bullets = [b for b in self.bullets
                        if not b.off_screen and not b.dead]
    def _update_effects(self, dt):
        for effect in self.effects:
            effect.update(dt)
        self.effects = [e for e in self.effects if not e.expired]
    # --------------------------------------------------------- collisions
    def _check_collisions(self):
        if not self.fleet:
            return
        # Player bullets vs aliens
        for bullet in self.bullets:
            if bullet.dead:
                continue
            for alien in self.fleet.aliens:
                if bullet.rect.colliderect(alien.rect):
                    bullet.dead = True
                    self.fleet.aliens.remove(alien)
                    self.stats.add_score(alien.points)
                    self.effects.append(Explosion(
                        alien.rect.center, alien.color,
                        self.settings.explosion_duration))
                    break
        if self.state != 'playing':
            return
        # Alien bombs vs ship
        for bomb in self.fleet.bombs:
            if bomb.rect.colliderect(self.ship.rect):
                self.fleet.bombs.remove(bomb)
                self._ship_hit()
                break
        # Aliens colliding with the ship directly
        for alien in self.fleet.aliens:
            if alien.rect.colliderect(self.ship.rect):
                self._ship_hit()
                break
    def _check_game_conditions(self):
        if self.state != 'playing':
            return
        # Aliens reached the bottom -> game over
        if self.fleet.reached_bottom():
            self.stats.lives = 0
            self.state = 'game_over'
            return
        # All aliens destroyed -> next wave
        if not self.fleet.aliens:
            self.fleet.bombs = []
            self.wave_clear_timer = self.settings.wave_clear_pause
            self.state = 'wave_clear'
    def _ship_hit(self):
        self.stats.lives -= 1
        self.flash_timer = self.settings.flash_duration
        self.effects.append(Explosion(self.ship.rect.center,
                                      self.settings.ship_color,
                                      duration=0.6, particles=18))
        self.fleet.bombs = []
        self.bullets = []
        if self.stats.lives <= 0:
            self.state = 'game_over'
        else:
            self.ship.center_ship()
    # ------------------------------------------------------------- states
    def _start_game(self):
        self.stats.reset()
        self.bullets = []
        self.ship.center_ship()
        self.effects = []
        self.flash_timer = 0
        self._spawn_fleet()
        self.state = 'playing'
    def _spawn_fleet(self):
        self.fleet = Fleet(self, self.stats.level)
    # --------------------------------------------------------------- draw
    def _update_screen(self):
        self.screen.fill(self.settings.bg_color)
        self.ship.draw()
        if self.fleet:
            self.fleet.draw(self.screen)
        for bullet in self.bullets:
            bullet.draw(self.screen)
        for effect in self.effects:
            effect.draw(self.screen)
        self.scoreboard.show_score()
        self._draw_flash()
        if self.state == 'start':
            self._draw_message("SPACE INVADERS", "Press SPACE to start")
        elif self.state == 'game_over':
            self._draw_message("GAME OVER",
                               f"Score: {self.stats.score}  -  Press SPACE to restart")
        elif self.state == 'wave_clear':
            self._draw_message(f"WAVE {self.stats.level} CLEARED!", "Get ready...")
        elif self.state == 'paused':
            self._draw_message("PAUSED", "Press P to resume")
        pygame.display.flip()
    def _draw_flash(self):
        if self.flash_timer > 0:
            w, h = self.screen.get_size()
            alpha = int(120 * (self.flash_timer / self.settings.flash_duration))
            overlay = pygame.Surface((w, h))
            overlay.set_alpha(alpha)
            overlay.fill((255, 40, 40))
            self.screen.blit(overlay, (0, 0))
    def _draw_message(self, title, subtitle=""):
        w, h = self.screen.get_size()
        title_img = self.big_font.render(title, True, (230, 235, 255))
        rect = title_img.get_rect(center=(w // 2, h // 2 - 30))
        overlay = pygame.Surface((w, h), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 140))
        self.screen.blit(overlay, (0, 0))
        self.screen.blit(title_img, rect)
        if subtitle:
            sub_img = self.small_font.render(subtitle, True, (180, 190, 220))
            sub_rect = sub_img.get_rect(center=(w // 2, h // 2 + 30))
            self.screen.blit(sub_img, sub_rect)