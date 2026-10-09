'''
game.py
Core game class: owns the pygame window, sprite groups, score/lives,
the main loop, collision handling, HUD rendering and the game-over /
victory / restart flow.
'''
import sys
import pygame
import settings
from sprites import Player
from fleet import Fleet
class Game:
    """Main application: window, game state, loop and rendering."""
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((settings.WIDTH, settings.HEIGHT))
        pygame.display.set_caption(settings.TITLE)
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(settings.FONT_NAME, settings.HUD_FONT_SIZE)
        self.big_font = pygame.font.Font(settings.FONT_NAME, settings.BIG_FONT_SIZE)
        self.reset()
    def reset(self):
        """(Re)start a fresh game."""
        self.player = Player()
        self.players = pygame.sprite.GroupSingle(self.player)
        self.bullets = pygame.sprite.Group()
        self.bombs = pygame.sprite.Group()
        self.fleet = Fleet(self.bombs)
        self.score = 0
        self.lives = settings.STARTING_LIVES
        self.state = "playing"  # playing / game_over / victory
    # ------------------------------------------------------------------
    # Main loop
    # ------------------------------------------------------------------
    def run(self):
        """Main game loop: events -> update -> draw, capped at FPS."""
        while True:
            self.handle_events()
            if self.state == "playing":
                self.update()
            self.draw()
            self.clock.tick(settings.FPS)
    def handle_events(self):
        """Handle quit, firing (SPACE) and restarting (R)."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and self.state == "playing":
                    bullet = self.player.shoot()
                    if bullet:
                        self.bullets.add(bullet)
                elif event.key == pygame.K_r and self.state != "playing":
                    self.reset()
    # ------------------------------------------------------------------
    # Update / collisions
    # ------------------------------------------------------------------
    def update(self):
        """Update all sprites and resolve collisions / end conditions."""
        self.players.update()
        self.bullets.update()
        self.bombs.update()
        self.fleet.update()
        # Player bullets destroy aliens and score points
        hits = pygame.sprite.groupcollide(self.bullets, self.fleet.aliens, True, True)
        for aliens in hits.values():
            for alien in aliens:
                self.score += alien.points
        # Alien bombs hit the player: lose a life and respawn the ship
        if pygame.sprite.spritecollide(self.player, self.bombs, True):
            self.lives -= 1
            self.player.rect.midbottom = (settings.PLAYER_START_X, settings.PLAYER_START_Y)
            if self.lives <= 0:
                self.state = "game_over"
        # Aliens reached the defense line: game over
        if self.state == "playing" and self.fleet.has_reached(settings.ALIEN_REACH_Y):
            self.state = "game_over"
        # All aliens destroyed: victory
        if self.state == "playing" and not self.fleet.aliens:
            self.state = "victory"
    # ------------------------------------------------------------------
    # Rendering
    # ------------------------------------------------------------------
    def draw(self):
        """Render the scene, HUD and (if needed) end-of-game messages."""
        self.screen.fill(settings.BLACK)
        self.players.draw(self.screen)
        self.fleet.aliens.draw(self.screen)
        self.bullets.draw(self.screen)
        self.bombs.draw(self.screen)
        self.draw_hud()
        if self.state == "game_over":
            self.draw_center_text("GAME OVER", settings.RED,
                                  sub="Press R to restart")
        elif self.state == "victory":
            self.draw_center_text("VICTORY!", settings.GREEN,
                                  sub=f"Final score: {self.score} - Press R to play again")
        pygame.display.flip()
    def draw_hud(self):
        """Show score (top-left) and remaining lives (top-right)."""
        score_surf = self.font.render(f"Score: {self.score}", True, settings.WHITE)
        lives_surf = self.font.render(f"Lives: {self.lives}", True, settings.GREEN)
        self.screen.blit(score_surf, (10, 10))
        self.screen.blit(lives_surf,
                         (settings.WIDTH - lives_surf.get_width() - 10, 10))
    def draw_center_text(self, text, color, sub=None):
        """Blit a big centered message with an optional smaller subtitle."""
        surf = self.big_font.render(text, True, color)
        rect = surf.get_rect(center=(settings.WIDTH // 2, settings.HEIGHT // 2 - 20))
        self.screen.blit(surf, rect)
        if sub:
            sub_surf = self.font.render(sub, True, settings.WHITE)
            sub_rect = sub_surf.get_rect(center=(settings.WIDTH // 2, settings.HEIGHT // 2 + 30))
            self.screen.blit(sub_surf, sub_rect)