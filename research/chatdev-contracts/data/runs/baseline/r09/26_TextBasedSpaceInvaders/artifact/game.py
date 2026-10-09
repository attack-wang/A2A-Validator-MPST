'''
game.py
Core game object: owns the pygame window and clock, wires together
settings, stats, ship, fleet, bullets and scoreboard, runs the main
loop and implements event handling, collisions, life loss, level
progression and all drawing.
'''
import sys
import pygame
import settings
from alien import AlienFleet
from bullet import PlayerBullet, EnemyBullet
from game_stats import GameStats
from scoreboard import Scoreboard
from ship import Ship
class SpaceInvadersGame:
    def __init__(self):
        pygame.init()
        self.settings = settings
        self.screen = pygame.display.set_mode(
            (self.settings.SCREEN_WIDTH, self.settings.SCREEN_HEIGHT))
        pygame.display.set_caption(self.settings.WINDOW_TITLE)
        self.clock = pygame.time.Clock()
        self.stats = GameStats(self.settings)
        self.scoreboard = Scoreboard(self.settings, self.screen, self.stats)
        self.ship = Ship(self.settings, self.screen)
        self.fleet = AlienFleet(self.settings, self.screen)
        self.player_bullets = []
        self.enemy_bullets = []
    def run(self):
        while True:
            dt = self.clock.tick(self.settings.FPS) / 1000.0
            dt = min(dt, 0.05)  # clamp to avoid huge jumps
            self._check_events()
            if self.stats.game_active:
                self._update_game(dt)
            self._update_screen()
    def _check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._on_keydown(event.key)
            elif event.type == pygame.KEYUP:
                self._on_keyup(event.key)
    def _on_keydown(self, key):
        if key in (pygame.K_LEFT, pygame.K_a):
            self.ship.moving_left = True
        elif key in (pygame.K_RIGHT, pygame.K_d):
            self.ship.moving_right = True
        elif key == pygame.K_SPACE:
            if self.stats.game_active:
                self._fire_bullet()
            else:
                self._start_game()
        elif key == pygame.K_r and self.stats.game_over:
            self._start_game()
        elif key == pygame.K_q:
            pygame.quit()
            sys.exit()
    def _on_keyup(self, key):
        if key in (pygame.K_LEFT, pygame.K_a):
            self.ship.moving_left = False
        elif key in (pygame.K_RIGHT, pygame.K_d):
            self.ship.moving_right = False
    def _fire_bullet(self):
        """Fire a player bullet if allowed by cooldown and bullet cap."""
        if self.ship.can_fire() and len(self.player_bullets) < self.settings.MAX_PLAYER_BULLETS:
            bullet = PlayerBullet(self.settings, self.screen,
                                  self.ship.rect.centerx, self.ship.rect.top)
            self.player_bullets.append(bullet)
            self.ship.start_cooldown()
    def _start_game(self):
        """Reset stats and entities, then begin a fresh round."""
        self.stats.reset()
        self.stats.game_active = True
        self.fleet = AlienFleet(self.settings, self.screen)
        self.player_bullets = []
        self.enemy_bullets = []
        self.ship.reset_position()
    def _update_game(self, dt):
        """Advance the simulation one frame."""
        self.ship.update(dt)
        # Fleet movement; a drop may push aliens into the ship.
        self.fleet.update(dt)
        # Enemy fire.
        bomb = self.fleet.try_fire(dt)
        if bomb is not None:
            self.enemy_bullets.append(bomb)
        # Bullets.
        for bullet in self.player_bullets:
            bullet.update(dt)
        for bullet in self.enemy_bullets:
            bullet.update(dt)
        self._handle_collisions()
        # Remove spent bullets.
        self.player_bullets = [b for b in self.player_bullets if not b.off_screen()]
        self.enemy_bullets = [b for b in self.enemy_bullets if not b.off_screen()]
        # Win condition: every alien destroyed.
        if not self.fleet.aliens and self.stats.game_active:
            self.stats.game_active = False
            self.stats.game_over = True
            self.stats.game_won = True
        # Lose condition: aliens reached the ship's level.
        if self.fleet.reached_bottom(self.ship.rect.top) and self.stats.game_active:
            self._lose_life()
    def _handle_collisions(self):
        """Bullet-vs-alien and bomb-vs-ship collisions."""
        # Player bullets vs aliens.
        for bullet in self.player_bullets[:]:
            for alien in self.fleet.aliens:
                if bullet.rect.colliderect(alien.rect):
                    self.stats.add_score(alien.points)
                    self.fleet.aliens.remove(alien)
                    self.player_bullets.remove(bullet)
                    break
        # Enemy bullets vs ship.
        for bullet in self.enemy_bullets[:]:
            if bullet.rect.colliderect(self.ship.rect):
                self.enemy_bullets.remove(bullet)
                self._lose_life()
    def _lose_life(self):
        """Consume a life; end the game when none remain."""
        if self.stats.lose_life():
            self.stats.game_active = False
            self.stats.game_over = True
            self.stats.game_won = False
        else:
            # Brief reprieve: clear bullets and push the fleet back up.
            self.player_bullets = []
            self.enemy_bullets = []
            for alien in self.fleet.aliens:
                alien.move(0, -self.settings.FLEET_DROP_DISTANCE * 2)
    def _update_screen(self):
        """Redraw the whole frame."""
        self.screen.fill(self.settings.COLOR_BACKGROUND)
        pygame.draw.rect(
            self.screen, self.settings.COLOR_GROUND,
            (0, self.settings.SCREEN_HEIGHT - 10, self.settings.SCREEN_WIDTH, 10))
        self.fleet.draw()
        for bullet in self.player_bullets:
            bullet.draw()
        for bullet in self.enemy_bullets:
            bullet.draw()
        self.ship.draw()
        self.scoreboard.draw(self.ship.image)
        if not self.stats.game_active:
            if self.stats.game_over:
                if self.stats.game_won:
                    self.scoreboard.draw_message("VICTORY!", "Press R to play again")
                else:
                    self.scoreboard.draw_message("GAME OVER", "Press R to play again")
            else:
                self.scoreboard.draw_message(
                    "SPACE INVADERS", "Press SPACE to start - Move: A/D or Arrows, Fire: SPACE")
        pygame.display.flip()