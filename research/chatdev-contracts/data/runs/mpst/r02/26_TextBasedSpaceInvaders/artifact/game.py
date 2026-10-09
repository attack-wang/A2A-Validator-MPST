'''Core game loop: events, updates, collisions, and rendering.'''
import sys
import pygame
from settings import (SCREEN_WIDTH, SCREEN_HEIGHT, FPS, BLACK, WHITE,
                      SHIP_LIVES)
from ship import Ship
from bullet import Bullet
from fleet import AlienFleet
from game_stats import GameStats, STATE_PLAYING, STATE_GAME_OVER, STATE_WIN
from hud import HUD
class Game:
    '''Coordinates all game objects and runs the main loop.'''
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Space Invaders")
        self.clock = pygame.time.Clock()
        self.hud = HUD()
        self.stats = GameStats()
        self.ship = Ship()
        self.fleet = AlienFleet()
        self.player_bullets = pygame.sprite.Group()
        self.alien_bullets = pygame.sprite.Group()
        self.fleet.create()
    def run(self):
        '''Main game loop.'''
        while True:
            self._handle_events()
            if self.stats.state == STATE_PLAYING:
                self._update()
            self._draw()
            self.clock.tick(FPS)
    def _handle_events(self):
        '''Process keyboard and window events.'''
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and self.stats.state == STATE_PLAYING:
                    self._ship_shoot()
                elif event.key in (pygame.K_RETURN, pygame.K_r) and self.stats.state != STATE_PLAYING:
                    self._restart()
                elif event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
    def _ship_shoot(self):
        '''Fire a bullet from the ship if under the on-screen limit.'''
        if len(self.player_bullets) < self.ship.bullet_limit:
            bullet = Bullet(self.ship.rect.centerx, self.ship.rect.top, going_up=True)
            self.player_bullets.add(bullet)
    def _update(self):
        '''Update all game objects and resolve collisions.'''
        self.ship.update()
        self.fleet.update()
        self.player_bullets.update()
        self.alien_bullets.update()
        # Alien fire
        shot = self.fleet.fire()
        if shot:
            x, y = shot
            self.alien_bullets.add(Bullet(x, y, going_up=False))
        self._check_player_bullet_hits()
        self._check_alien_bullet_hits()
        self._check_invasion()
    def _check_player_bullet_hits(self):
        '''Destroy aliens hit by player bullets and award points.'''
        collisions = pygame.sprite.groupcollide(
            self.player_bullets, self.fleet.aliens, True, True)
        for aliens_hit in collisions.values():
            for alien in aliens_hit:
                self.stats.score += alien.points
                self.fleet.speed_up()
        if not self.fleet.aliens and self.stats.state == STATE_PLAYING:
            self.stats.state = STATE_WIN
    def _check_alien_bullet_hits(self):
        '''Handle alien bullets hitting the ship or reaching the ground.'''
        hits = pygame.sprite.spritecollide(
            self.ship, self.alien_bullets, True)
        if hits:
            self._lose_life()
        # Alien bullets that hit the "ground" line just vanish (handled in Bullet.update)
    def _check_invasion(self):
        '''End the game if aliens reach the ship's line.'''
        invasion_line = self.ship.rect.top
        if self.fleet.reached_bottom(invasion_line):
            self.stats.lives = 0
            self.stats.state = STATE_GAME_OVER
    def _lose_life(self):
        '''Subtract a life; end the game when lives run out.'''
        self.stats.lives -= 1
        if self.stats.lives <= 0:
            self.stats.state = STATE_GAME_OVER
        else:
            self.ship.center_ship()
            self.alien_bullets.empty()
    def _restart(self):
        '''Reset everything for a new game.'''
        self.stats.reset()
        self.player_bullets.empty()
        self.alien_bullets.empty()
        self.fleet.create()
        self.ship.center_ship()
    def _draw(self):
        '''Render background, sprites, HUD, and end messages.'''
        self.screen.fill(BLACK)
        for sprite in self.fleet.aliens:
            self.screen.blit(sprite.image, sprite.rect)
        self.screen.blit(self.ship.image, self.ship.rect)
        for bullet in self.player_bullets:
            self.screen.blit(bullet.image, bullet.rect)
        for bullet in self.alien_bullets:
            self.screen.blit(bullet.image, bullet.rect)
        self.hud.draw(self.screen, self.stats.score, self.stats.lives)
        if self.stats.state == STATE_GAME_OVER:
            self.hud.draw_center_message(
                self.screen, "GAME OVER",
                f"Final score: {self.stats.score} - Press ENTER to play again")
        elif self.stats.state == STATE_WIN:
            self.hud.draw_center_message(
                self.screen, "YOU WIN!",
                f"Final score: {self.stats.score} - Press ENTER to play again")
        pygame.display.flip()