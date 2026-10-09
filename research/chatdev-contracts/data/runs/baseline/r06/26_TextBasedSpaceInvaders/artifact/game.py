'''
game.py
Core game class: main loop, state machine (playing / game over /
victory), input handling, collision detection and rendering.
'''
import sys
import pygame
import settings
from player import Player
from alien import AlienFleet
from bullet import Bullet, Bomb
from scoreboard import Scoreboard
class Game:
    STATE_PLAYING = "playing"
    STATE_GAME_OVER = "game_over"
    STATE_VICTORY = "victory"
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode(
            (settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT))
        pygame.display.set_caption(settings.TITLE)
        self.clock = pygame.time.Clock()
        self.font_big = pygame.font.SysFont(None, settings.FONT_SIZE_LARGE)
        self.font_small = pygame.font.SysFont(None, settings.FONT_SIZE_SMALL)
        self.scoreboard = Scoreboard()
        self.reset()
    def reset(self):
        """(Re)initialise all gameplay objects for a fresh round."""
        self.player = Player()
        self.fleet = AlienFleet()
        self.bullets = []
        self.bombs = []
        self.lives = settings.PLAYER_LIVES
        self.state = Game.STATE_PLAYING
        self.scoreboard.reset()
    def run(self):
        """Main game loop."""
        while True:
            dt = min(self.clock.tick(settings.FPS) / 1000.0,
                     settings.MAX_DELTA_TIME)
            self.handle_events()
            if self.state == Game.STATE_PLAYING:
                self.update(dt)
            self.draw()
            pygame.display.flip()
    def handle_events(self):
        """Process the event queue (quit, shooting, restart)."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self._quit()
            elif event.type == pygame.KEYDOWN:
                if self.state == Game.STATE_PLAYING and event.key == pygame.K_SPACE:
                    self.player_shoot()
                elif (self.state in (Game.STATE_GAME_OVER, Game.STATE_VICTORY)
                      and event.key in (pygame.K_r, pygame.K_RETURN)):
                    self.reset()
                elif event.key == pygame.K_ESCAPE:
                    self._quit()
    def _quit(self):
        """Save the high score and exit cleanly."""
        self.scoreboard.save_high_score()
        pygame.quit()
        sys.exit()
    def player_shoot(self):
        """Fire a bullet if cooldown and magazine allow."""
        if self.player.can_shoot() and len(self.bullets) < settings.MAX_PLAYER_BULLETS:
            self.bullets.append(self.player.shoot())
    def update(self, dt):
        """Advance the simulation one frame."""
        self.player.update(dt)
        for b in self.bullets:
            b.update(dt)
        for bomb in self.bombs:
            bomb.update(dt)
        new_bomb = self.fleet.update(dt)
        if new_bomb is not None:
            self.bombs.append(new_bomb)
        self.check_collisions()
        self.cleanup()
        self.check_game_conditions()
    def check_collisions(self):
        """Handle bullet-alien, bullet-bomb, bomb-player and invasion checks."""
        # bullets vs aliens
        for bullet in self.bullets:
            if not bullet.alive:
                continue
            for alien in self.fleet.alive_aliens:
                if bullet.rect.colliderect(alien.rect):
                    bullet.alive = False
                    alien.alive = False
                    self.scoreboard.add_points(alien.points)
                    break
        # bullets vs bombs (shoot down incoming bombs)
        for bullet in self.bullets:
            if not bullet.alive:
                continue
            for bomb in self.bombs:
                if bomb.alive and bullet.rect.colliderect(bomb.rect):
                    bullet.alive = False
                    bomb.alive = False
                    self.scoreboard.add_points(5)  # small bonus
        # bombs vs player
        for bomb in self.bombs:
            if bomb.alive and not self.player.is_invulnerable() \
                    and bomb.rect.colliderect(self.player.rect):
                bomb.alive = False
                self.lose_life()
        # aliens reaching the player's line -> invasion, game over
        for alien in self.fleet.alive_aliens:
            if alien.rect.bottom >= self.player.rect.top:
                self.state = Game.STATE_GAME_OVER
                return
    def lose_life(self):
        """Subtract a life; end the game when none remain."""
        self.lives -= 1
        if self.lives <= 0:
            self.state = Game.STATE_GAME_OVER
        else:
            self.player.hit()
    def cleanup(self):
        """Remove deactivated bullets and bombs."""
        self.bullets = [b for b in self.bullets if b.alive]
        self.bombs = [b for b in self.bombs if b.alive]
    def check_game_conditions(self):
        """Victory when every alien has been destroyed."""
        if self.state == Game.STATE_PLAYING and not self.fleet.alive_aliens:
            self.state = Game.STATE_VICTORY
    def draw(self):
        """Render the current frame based on game state."""
        self.screen.fill(settings.BLACK)
        if self.state in (Game.STATE_PLAYING, Game.STATE_GAME_OVER,
                          Game.STATE_VICTORY):
            self.fleet.draw(self.screen)
            self.player.draw(self.screen)
            for b in self.bullets:
                b.draw(self.screen)
            for bomb in self.bombs:
                bomb.draw(self.screen)
            self.scoreboard.draw(self.screen, self.lives)
        if self.state == Game.STATE_GAME_OVER:
            self._draw_center_text("GAME OVER", settings.RED,
                                   "Press R or ENTER to restart")
        elif self.state == Game.STATE_VICTORY:
            self._draw_center_text("VICTORY!", settings.GREEN,
                                   "Press R or ENTER to play again")
    def _draw_center_text(self, title, color, subtitle):
        """Blit a translucent overlay with a title and subtitle."""
        overlay = pygame.Surface((settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT),
                                 pygame.SRCALPHA)
        overlay.fill(settings.OVERLAY)
        self.screen.blit(overlay, (0, 0))
        title_surf = self.font_big.render(title, True, color)
        self.screen.blit(title_surf,
                         (settings.SCREEN_WIDTH // 2 - title_surf.get_width() // 2,
                          settings.SCREEN_HEIGHT // 2 - 60))
        sub_surf = self.font_small.render(subtitle, True, settings.WHITE)
        self.screen.blit(sub_surf,
                         (settings.SCREEN_WIDTH // 2 - sub_surf.get_width() // 2,
                          settings.SCREEN_HEIGHT // 2 + 10))
        score_surf = self.font_small.render(
            f"Final score: {self.scoreboard.score}", True, settings.YELLOW)
        self.screen.blit(score_surf,
                         (settings.SCREEN_WIDTH // 2 - score_surf.get_width() // 2,
                          settings.SCREEN_HEIGHT // 2 + 44))