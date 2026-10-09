'''
game.py
-------
Core game object: owns the pygame window, the sprite groups,
score/lives/wave state, collision handling and the main loop
including the playing, game-over and victory screens.
'''
import sys
import pygame
import settings
from player import Player
from alien import AlienFleet
class Game:
    '''Runs one session of Space Invaders.'''
    def __init__(self):
        '''Create the window, fonts and initial game state.'''
        pygame.init()
        self.screen = pygame.display.set_mode((settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT))
        pygame.display.set_caption(settings.CAPTION)
        self.clock = pygame.time.Clock()
        self.font_big = pygame.font.SysFont(None, 64)
        self.font_small = pygame.font.SysFont(None, 32)
        self.reset()
    def reset(self):
        '''(Re)initialise all gameplay state for a fresh session.'''
        self.player = Player()
        self.player_bullets = pygame.sprite.Group()
        self.alien_bullets = pygame.sprite.Group()
        self.wave = 1
        self.score = 0
        self.lives = settings.STARTING_LIVES
        self.fleet = AlienFleet()
        self.state = "playing"   # "playing" | "game_over" | "victory"
    # ----- wave / life management -----
    def next_wave(self):
        '''All aliens destroyed: start a faster, more aggressive wave.'''
        self.wave += 1
        self.fleet = AlienFleet(speed_multiplier=settings.FLEET_SPEEDUP ** (self.wave - 1))
        self.player_bullets.empty()
        self.alien_bullets.empty()
    def lose_life(self):
        '''Player was hit: respawn (with grace period) or end the game.'''
        self.lives -= 1
        self.alien_bullets.empty()
        if self.lives <= 0:
            self.state = "game_over"
        else:
            self.player.rect.midbottom = (settings.PLAYER_START_X, settings.SCREEN_HEIGHT - 20)
            self.player.invincible = settings.PLAYER_RESPAWN_INVINCIBILITY
    # ----- collisions -----
    def handle_collisions(self):
        '''Player bullets vs aliens, bombs vs player, bottom-line and victory checks.'''
        hits = pygame.sprite.groupcollide(self.player_bullets, self.fleet.aliens, True, True)
        for bullet, aliens in hits.items():
            for alien in aliens:
                self.score += alien.value()
        if self.player.invincible == 0:
            if pygame.sprite.spritecollide(self.player, self.alien_bullets, True):
                self.lose_life()
        if self.fleet.reached_bottom():
            self.state = "game_over"
        elif self.fleet.empty():
            # Victory when the final wave is cleared, otherwise advance a wave.
            if self.wave >= settings.TOTAL_WAVES:
                self.state = "victory"
            else:
                self.next_wave()
    # ----- events -----
    def handle_events(self):
        '''Process quit, shooting and restart input.'''
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if self.state == "playing":
                    if event.key == pygame.K_SPACE:
                        bullet = self.player.shoot()
                        if bullet:
                            self.player_bullets.add(bullet)
                else:  # game_over or victory
                    if event.key in (pygame.K_r, pygame.K_SPACE):
                        self.reset()
    # ----- per-frame update -----
    def update(self):
        '''Advance the simulation one frame while playing.'''
        if self.state != "playing":
            return
        self.player.update()
        bomb = self.fleet.drop_bomb()          # fleet may drop a bomb this frame
        if bomb:
            self.alien_bullets.add(bomb)
        self.player_bullets.update()
        self.alien_bullets.update()
        self.fleet.update()
        self.handle_collisions()
    # ----- drawing -----
    def draw_hud(self):
        '''Show score, lives and wave counter at the top of the screen.'''
        score_surf = self.font_small.render(f"Score: {self.score}", True, settings.COLOR_WHITE)
        lives_surf = self.font_small.render(f"Lives: {self.lives}", True, settings.COLOR_WHITE)
        wave_surf = self.font_small.render(f"Wave: {self.wave}/{settings.TOTAL_WAVES}",
                                           True, settings.COLOR_WHITE)
        self.screen.blit(score_surf, (10, 10))
        self.screen.blit(lives_surf, (10, 40))
        self.screen.blit(wave_surf, (settings.SCREEN_WIDTH - wave_surf.get_width() - 10, 10))
    def draw_end_screen(self, text, color):
        '''Overlay an end-of-game message and restart hint on a dimmed play field.'''
        overlay = pygame.Surface((settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT))
        overlay.set_alpha(180)
        overlay.fill(settings.COLOR_BACKGROUND)
        self.screen.blit(overlay, (0, 0))
        title = self.font_big.render(text, True, color)
        hint = self.font_small.render("Press R or SPACE to play again", True, settings.COLOR_WHITE)
        self.screen.blit(title, title.get_rect(center=(settings.SCREEN_WIDTH // 2,
                                                       settings.SCREEN_HEIGHT // 2 - 20)))
        self.screen.blit(hint, hint.get_rect(center=(settings.SCREEN_WIDTH // 2,
                                                     settings.SCREEN_HEIGHT // 2 + 40)))
    def draw(self):
        '''Render one full frame: field, sprites, HUD and end screens.'''
        self.screen.fill(settings.COLOR_BACKGROUND)
        self.fleet.aliens.draw(self.screen)
        self.player_bullets.draw(self.screen)
        self.alien_bullets.draw(self.screen)
        self.player.draw(self.screen)
        self.draw_hud()
        if self.state == "game_over":
            self.draw_end_screen("GAME OVER", settings.COLOR_RED)
        elif self.state == "victory":
            self.draw_end_screen("YOU WIN!", settings.COLOR_GREEN)
        pygame.display.flip()
    # ----- main loop -----
    def run(self):
        '''Main game loop: events, update and draw at a fixed frame rate.'''
        while True:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(settings.FPS)