'''
Main game class: state machine, input handling, collision and rendering.
'''
import sys
import pygame
import settings
from background import Background
from bird import Bird
from highscore import HighScore
from pipe_manager import PipeManager
from sounds import SoundFactory
STATE_READY = 'ready'
STATE_PLAYING = 'playing'
STATE_GAME_OVER = 'game_over'
class Game:
    """Top-level application: owns the game loop and all subsystems."""
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode(
            (settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT))
        pygame.display.set_caption(settings.TITLE)
        self.clock = pygame.time.Clock()
        self.font_big = pygame.font.Font(None, 52)
        self.font_small = pygame.font.Font(None, 26)
        self.sounds = SoundFactory()
        self.sounds.build()
        self.background = Background()
        self.highscore = HighScore()
        self.best = self.highscore.load()
        self.state = STATE_READY
        self.score = 0
        self.flash_timer = 0.0
        self.game_over_timer = 0.0
        self._reset_round()
    def _reset_round(self):
        """Reset bird, pipes and score for a fresh attempt."""
        self.bird = Bird(settings.BIRD_X, settings.SCREEN_HEIGHT * 0.45)
        self.pipes = PipeManager()
        self.score = 0
    def run(self):
        """Main loop: events -> update -> render, with clamped dt."""
        while True:
            # Clamp dt so a window drag / stall can't cause tunneling.
            dt = min(self.clock.tick(settings.FPS) / 1000.0, 1.0 / 30.0)
            self._handle_events()
            self._update(dt)
            self._draw()
    def _handle_events(self):
        """Process quit / flap / restart input."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                elif event.key in (pygame.K_SPACE, pygame.K_UP):
                    self._flap()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                self._flap()
    def _flap(self):
        """Dispatch flap input according to the current state."""
        if self.state == STATE_READY:
            self.state = STATE_PLAYING
            self.bird.flap()
            self.sounds.play('flap')
        elif self.state == STATE_PLAYING:
            self.bird.flap()
            self.sounds.play('flap')
        elif self.state == STATE_GAME_OVER and self.game_over_timer > 0.6:
            # Small delay prevents an accidental instant restart.
            self._reset_round()
            self.state = STATE_READY
    def _update(self, dt):
        """Advance the simulation for the current state."""
        if self.state == STATE_READY:
            self.bird.idle_hover(dt)
            self.background.update(dt, 0)
        elif self.state == STATE_PLAYING:
            self.bird.update(dt)
            self.pipes.update(dt, self.score)
            passed = self.pipes.pipes_passed(settings.BIRD_X)
            if passed:
                self.score += passed
                self.sounds.play('score')
            self.background.update(dt, self.pipes.current_speed(self.score))
            # Keep the bird under the ceiling (prevents flying over pipes).
            if self.bird.y < settings.BIRD_RADIUS:
                self.bird.y = settings.BIRD_RADIUS
                self.bird.velocity = max(self.bird.velocity, 0.0)
            # Collision checks: pipes and ground.
            ground_top = settings.SCREEN_HEIGHT - settings.GROUND_HEIGHT
            hit_pipe = self.pipes.collides(self.bird.get_rect())
            hit_ground = self.bird.y + settings.BIRD_RADIUS >= ground_top
            if hit_pipe or hit_ground:
                self._game_over(hit_ground)
        elif self.state == STATE_GAME_OVER:
            self.game_over_timer += dt
            ground_top = settings.SCREEN_HEIGHT - settings.GROUND_HEIGHT
            floor_y = ground_top - settings.BIRD_RADIUS
            if self.bird.y < floor_y:
                self.bird.update(dt)
                if self.bird.y >= floor_y:
                    self.bird.y = floor_y
                    self.bird.velocity = 0
                    self.bird.rotation = 90
            self.background.update(dt, 0)
        if self.flash_timer > 0:
            self.flash_timer = max(0.0, self.flash_timer - dt)
    def _game_over(self, hit_ground):
        """Switch to the game-over state, save the best score."""
        self.state = STATE_GAME_OVER
        self.game_over_timer = 0.0
        self.flash_timer = 0.25
        self.sounds.play('hit')
        if hit_ground:
            ground_top = settings.SCREEN_HEIGHT - settings.GROUND_HEIGHT
            self.bird.y = ground_top - settings.BIRD_RADIUS
            self.bird.velocity = 0
            self.bird.rotation = 90
        if self.score > self.best:
            self.best = self.score
            self.highscore.save(self.best)
    def _draw(self):
        """Render the whole frame in back-to-front order."""
        self.background.draw(self.screen)
        self.pipes.draw(self.screen)
        self.bird.draw(self.screen)
        self._draw_hud()
        if self.flash_timer > 0:
            flash = pygame.Surface((settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT), pygame.SRCALPHA)
            flash.fill((255, 255, 255, int(180 * (self.flash_timer / 0.25))))
            self.screen.blit(flash, (0, 0))
        pygame.display.flip()
    def _draw_hud(self):
        """Score, ready-screen instructions and game-over panel."""
        if self.state == STATE_READY:
            self._draw_text('FLAPPY BIRD', self.font_big, settings.SCREEN_WIDTH / 2, settings.SCREEN_HEIGHT * 0.22)
            self._draw_text('Press SPACE / UP / click to flap', self.font_small,
                            settings.SCREEN_WIDTH / 2, settings.SCREEN_HEIGHT * 0.62)
            self._draw_text('Avoid the pipes and the ground!', self.font_small,
                            settings.SCREEN_WIDTH / 2, settings.SCREEN_HEIGHT * 0.68)
        else:
            self._draw_text(str(self.score), self.font_big, settings.SCREEN_WIDTH / 2, 60)
        if self.state == STATE_GAME_OVER and self.game_over_timer > 0.6:
            self._draw_text('GAME OVER', self.font_big, settings.SCREEN_WIDTH / 2, settings.SCREEN_HEIGHT * 0.32,
                            color=settings.GAME_OVER_COLOR)
            self._draw_text('Score: %d   Best: %d' % (self.score, self.best),
                            self.font_small, settings.SCREEN_WIDTH / 2, settings.SCREEN_HEIGHT * 0.40)
            self._draw_text('Press SPACE to play again', self.font_small,
                            settings.SCREEN_WIDTH / 2, settings.SCREEN_HEIGHT * 0.46)
    def _draw_text(self, text, font, x, y, color=None):
        """Blit centered text with a drop shadow."""
        color = settings.TEXT_COLOR if color is None else color
        shadow = font.render(text, True, settings.TEXT_SHADOW)
        rect = shadow.get_rect(center=(int(x) + 2, int(y) + 2))
        self.screen.blit(shadow, rect)
        label = font.render(text, True, color)
        rect = label.get_rect(center=(int(x), int(y)))
        self.screen.blit(label, rect)