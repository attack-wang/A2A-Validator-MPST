'''
alien_invasion.py — main controller that assembles every module and runs
the Space Invaders game loop (events, updates, collisions, drawing).
'''
import random
import pygame
from settings import Settings
from ship import Ship
from alien import Alien
from bullet import Bullet
from game_stats import GameStats
from scoreboard import Scoreboard
class AlienInvasion:
    '''Overall class that manages game assets, behavior and the main loop.'''
    def __init__(self):
        '''Initialize pygame, the window and every game object.'''
        pygame.init()
        self.settings = Settings()
        self.screen = pygame.display.set_mode(
            (self.settings.screen_width, self.settings.screen_height))
        pygame.display.set_caption(self.settings.caption)
        self.clock = pygame.time.Clock()
        # Dynamic data (score, lives, state) first, then objects that read it.
        self.stats = GameStats(self.settings)
        # Ship MUST be created before Scoreboard (scoreboard reuses ship image).
        self.ship = Ship(self)
        self.scoreboard = Scoreboard(self)
        self.player_bullets = pygame.sprite.Group()
        self.alien_bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()
        # Fonts used for the start / game-over / victory messages.
        self.title_font = pygame.font.SysFont(None, 56)
        self.text_font = pygame.font.SysFont(None, 30)
        self._create_fleet()
    def run_game(self):
        '''Run the main game loop until the player quits.'''
        while True:
            self._check_events()
            if self.stats.game_active:
                self.ship.update()
                self._update_bullets()
                self._update_aliens()
            self._update_screen()
            self.clock.tick(self.settings.fps)
    # ------------------------- event handling -------------------------
    def _check_events(self):
        '''Respond to keypresses and window close events.'''
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.stats.save_high_score()
                pygame.quit()
                raise SystemExit
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)
    def _check_keydown_events(self, event):
        '''Respond to key presses (move, fire, start/restart, quit).'''
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        elif event.key == pygame.K_SPACE:
            if self.stats.game_active:
                self._fire_bullet()
            else:
                self._start_game()
        elif event.key == pygame.K_q:
            self.stats.save_high_score()
            pygame.quit()
            raise SystemExit
    def _check_keyup_events(self, event):
        '''Respond to key releases (stop movement).'''
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False
    def _start_game(self):
        '''(Re)start a fresh game: reset stats, fleet, bullets and ship.'''
        self.stats.reset_stats()
        self.stats.game_active = True
        self.settings.fleet_direction = 1   # reset direction persisted from last run
        self.aliens.empty()
        self.player_bullets.empty()
        self.alien_bullets.empty()
        self._create_fleet()
        self.ship.center_ship()
        self.scoreboard.prep_score()
        self.scoreboard.prep_lives()
    def _fire_bullet(self):
        '''Create a new player bullet if under the allowed limit.'''
        if len(self.player_bullets) < self.settings.bullets_allowed:
            new_bullet = Bullet(self, self.ship.rect.centerx,
                                self.ship.rect.top, -1)
            self.player_bullets.add(new_bullet)
    # ----------------------------- fleet ------------------------------
    def _create_fleet(self):
        '''Create the full grid of aliens (rows x cols).'''
        for row in range(self.settings.alien_rows):
            for col in range(self.settings.alien_cols):
                self.aliens.add(Alien(self, row, col))
    def _check_fleet_edges(self):
        '''Respond appropriately if any aliens have reached an edge.'''
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break
    def _change_fleet_direction(self):
        '''Drop the entire fleet and reverse its horizontal direction.'''
        for alien in self.aliens.sprites():
            alien.drop()
        self.settings.fleet_direction *= -1
    def _update_aliens(self):
        '''Move the fleet, let aliens fire, and check lose conditions.'''
        self._check_fleet_edges()
        self.aliens.update()
        self._alien_fire()
        # An alien colliding with the ship costs a life; the attacker is
        # destroyed too so the respawned ship is not hit again instantly.
        attacker = pygame.sprite.spritecollideany(self.ship, self.aliens)
        if attacker is not None:
            self.aliens.remove(attacker)
            self._ship_hit()
        # Aliens reaching the bottom end the game immediately.
        self._check_aliens_bottom()
    def _alien_fire(self):
        '''Give a random alien a per-frame chance to drop a bullet.'''
        if self.aliens and random.random() < self.settings.alien_fire_chance:
            shooter = random.choice(self.aliens.sprites())
            self.alien_bullets.add(Bullet(self, shooter.rect.centerx,
                                          shooter.rect.bottom, 1, is_alien=True))
    def _check_aliens_bottom(self):
        '''End the game if any alien reaches the bottom of the screen.'''
        screen_rect = self.screen.get_rect()
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= screen_rect.bottom:
                self._game_over()
                break
    # ---------------------------- bullets -----------------------------
    def _update_bullets(self):
        '''Move bullets, remove off-screen ones and resolve collisions.'''
        self.player_bullets.update()
        self.alien_bullets.update()
        # Delete bullets that have left the screen.
        for bullet in self.player_bullets.copy():
            if bullet.rect.bottom <= 0:
                self.player_bullets.remove(bullet)
        for bullet in self.alien_bullets.copy():
            if bullet.rect.top >= self.settings.screen_height:
                self.alien_bullets.remove(bullet)
        # Player bullets destroy aliens; award points based on the alien's row.
        collisions = pygame.sprite.groupcollide(
            self.player_bullets, self.aliens, True, True)
        if collisions:
            for aliens_hit in collisions.values():
                for alien in aliens_hit:
                    self.stats.score += self.settings.points_for_row(alien.row)
            self.scoreboard.prep_score()
            self.scoreboard.check_high_score()
        # Alien bullets can hit the ship.
        if pygame.sprite.spritecollideany(self.ship, self.alien_bullets):
            self._ship_hit()
        # Win condition: every alien has been destroyed.
        if self.stats.game_active and not self.aliens:
            self.stats.game_won = True
            self.stats.game_active = False
            self.stats.save_high_score()