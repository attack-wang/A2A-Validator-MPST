'''
Core game loop, state management, collisions, score and lives.
'''
import sys
import pygame
import settings
from ship import Ship
from alienfleet import AlienFleet
from ui import draw_hud, draw_center_text
STATE_PLAYING = "playing"
STATE_GAME_OVER = "game_over"
STATE_VICTORY = "victory"
class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT))
        pygame.display.set_caption(settings.TITLE)
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont(None, 28)
        self.big_font = pygame.font.SysFont(None, 64)
        self.score = 0
        self.lives = settings.SHIP_START_LIVES
        self.state = STATE_PLAYING
        self.ship = Ship()
        self.fleet = AlienFleet()
        self.player_bullets = []
        self.alien_bombs = []
        self._reset_entities()
    def _reset_entities(self):
        self.ship.reset()
        self.fleet = AlienFleet()
        self.player_bullets = []
        self.alien_bombs = []
    def run(self):
        while True:
            dt = self.clock.tick(settings.FPS) / 1000.0
            self._handle_events()
            if self.state == STATE_PLAYING:
                self._update(dt)
            self._draw()
    def _handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if self.state == STATE_PLAYING and event.key == pygame.K_SPACE:
                    bullet = self.ship.fire()
                    if bullet:
                        self.player_bullets.append(bullet)
                elif self.state in (STATE_GAME_OVER, STATE_VICTORY) and event.key == pygame.K_r:
                    self.score = 0
                    self.lives = settings.SHIP_START_LIVES
                    self.state = STATE_PLAYING
                    self._reset_entities()
    def _update(self, dt):
        keys = pygame.key.get_pressed()
        self.ship.update(dt, keys)
        for bullet in self.player_bullets:
            bullet.update(dt)
        self.player_bullets = [b for b in self.player_bullets if not b.is_offscreen()]
        self.alien_bombs.extend(self.fleet.update(dt))
        for bomb in self.alien_bombs:
            bomb.update(dt)
        self.alien_bombs = [b for b in self.alien_bombs if not b.is_offscreen()]
        self._check_collisions()
        if self.fleet.all_destroyed():
            self.state = STATE_VICTORY
        elif self.fleet.reached_bottom():
            self.state = STATE_GAME_OVER
    def _lose_life(self):
        self.lives -= 1
        if self.lives <= 0:
            self.state = STATE_GAME_OVER
        else:
            self.ship.reset()
            self.alien_bombs = []
    def _check_collisions(self):
        remaining_bullets = []
        for bullet in self.player_bullets:
            destroyed = False
            for alien in list(self.fleet.aliens):
                if bullet.rect.colliderect(alien.rect):
                    self.score += alien.points
                    self.fleet.aliens.remove(alien)
                    destroyed = True
                    break
            if not destroyed:
                remaining_bullets.append(bullet)
        self.player_bullets = remaining_bullets
        # Alien bombs vs ship: on a hit, lose a life and clear ALL bombs
        # so the player is not hit again immediately.
        surviving_bombs = []
        life_lost = False
        for bomb in self.alien_bombs:
            if not life_lost and bomb.rect.colliderect(self.ship.rect):
                self._lose_life()
                life_lost = True
            else:
                surviving_bombs.append(bomb)
        if life_lost:
            self.alien_bombs = []
        else:
            self.alien_bombs = surviving_bombs
    def _draw(self):
        self.screen.fill(settings.COLOR_BACKGROUND)
        for alien in self.fleet.aliens:
            alien.draw(self.screen)
        for bullet in self.player_bullets:
            bullet.draw(self.screen)
        for bomb in self.alien_bombs:
            bomb.draw(self.screen)
        self.ship.draw(self.screen)
        draw_hud(self.screen, self.font, self.score, self.lives)
        if self.state in (STATE_GAME_OVER, STATE_VICTORY):
            overlay = pygame.Surface((settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 160))
            self.screen.blit(overlay, (0, 0))
        if self.state == STATE_GAME_OVER:
            draw_center_text(self.screen, self.big_font, "GAME OVER", (255, 80, 80), -20)
            draw_center_text(self.screen, self.font,
                             f"Final Score: {self.score}  -  Press R to restart",
                             settings.COLOR_TEXT, 40)
        elif self.state == STATE_VICTORY:
            draw_center_text(self.screen, self.big_font, "VICTORY!", (120, 230, 120), -20)
            draw_center_text(self.screen, self.font,
                             f"Final Score: {self.score}  -  Press R to restart",
                             settings.COLOR_TEXT, 40)
        pygame.display.flip()