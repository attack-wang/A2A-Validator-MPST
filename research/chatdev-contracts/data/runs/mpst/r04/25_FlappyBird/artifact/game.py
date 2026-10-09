'''
game.py
The Game class wires everything together: the main loop, the
MENU / PLAYING / DYING / GAME_OVER state machine, event handling,
the static background artwork and per-state drawing.
'''
import math
import sys
import pygame
import settings
import sounds
from bird import Bird
from ground import Ground
from pipe_manager import PipeManager
from scoreboard import Scoreboard
MENU, PLAYING, DYING, GAME_OVER = 0, 1, 2, 3
class Game:
    """Top-level application: owns the window, states and all objects."""
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT))
        pygame.display.set_caption(settings.TITLE)
        self.clock = pygame.time.Clock()
        sounds.init()
        self.background = self._build_background()
        self.bird = Bird(settings.BIRD_X, settings.SKY_HEIGHT / 2)
        self.pipes = PipeManager()
        self.ground = Ground()
        self.scoreboard = Scoreboard()
        self.score = 0
        self.new_best = False
        self.state = MENU
        self.bob_timer = 0.0
    # -------------------------------------------------------- background
    @staticmethod
    def _draw_cloud(surface, cx, cy, scale):
        """Fluffy cloud made of three overlapping ellipses."""
        r = int(18 * scale)
        pygame.draw.ellipse(surface, settings.CLOUD_WHITE,
                            (cx - r, cy - r // 2, 2 * r, r))
        pygame.draw.ellipse(surface, settings.CLOUD_WHITE,
                            (cx - int(1.4 * r), cy, int(1.6 * r), int(0.9 * r)))
        pygame.draw.ellipse(surface, settings.CLOUD_WHITE,
                            (cx + int(0.2 * r), cy - int(0.2 * r), int(1.5 * r), int(0.9 * r)))
    def _build_background(self):
        """Pre-render the static sky, clouds and bush silhouette once."""
        bg = pygame.Surface((settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT))
        bg.fill(settings.SKY_BLUE)
        # clouds
        for cx, cy, s in [(60, 90, 1.0), (200, 60, 0.8), (360, 120, 1.1),
                          (120, 180, 0.7), (320, 220, 0.9)]:
            self._draw_cloud(bg, cx, cy, s)
        # distant bushes silhouette above the ground line
        for i in range(6):
            bx = 20 + i * 90
            by = settings.SKY_HEIGHT - 18
            pygame.draw.ellipse(bg, settings.BUSH_GREEN, (bx, by, 110, 40))
        return bg
    # ---------------------------------------------------------- main loop
    def run(self):
        """Standard game loop with a fixed maximum delta time."""
        dt = 0.0
        while True:
            dt = self.clock.tick(settings.FPS) / 1000.0
            dt = min(dt, 1 / 30)  # clamp to avoid tunneling after pauses
            self._handle_events()
            self.update(dt)
            self.draw()
    # ------------------------------------------------------------- events
    def _handle_events(self):
        """Keyboard/quit handling; SPACE drives every state transition."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_SPACE, pygame.K_UP):
                    if self.state == MENU:
                        self._start_playing()
                        self.bird.flap()
                        sounds.play("flap")
                    elif self.state == PLAYING:
                        self.bird.flap()
                        sounds.play("flap")
                    elif self.state == GAME_OVER:
                        self._reset_to_menu()
                elif event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
    # -------------------------------------------------------- transitions
    def _crash(self):
        """Pipe or ground hit while playing: start the death tumble."""
        sounds.play("hit")
        self.bird.alive = False
        self.state = DYING
        if self.bird.y < settings.SKY_HEIGHT - 40:
            sounds.play("fall")
    def _finish(self):
        """Bird has landed: record the score and show the game-over panel."""
        self.new_best = self.scoreboard.submit(self.score)
        self.state = GAME_OVER
    def _start_playing(self):
        """MENU → PLAYING with a fresh score and cleared pipes."""
        self.score = 0
        self.new_best = False
        self.pipes.reset()
        self.bird.reset(settings.BIRD_X, settings.SKY_HEIGHT / 2)
        self.state = PLAYING
    def _reset_to_menu(self):
        """GAME_OVER → MENU, ready for another round."""
        self.score = 0
        self.pipes.reset()
        self.bird.reset(settings.BIRD_X, settings.SKY_HEIGHT / 2)
        self.state = MENU
        self.bob_timer = 0.0
    # ------------------------------------------------------------- update
    def update(self, dt):
        """Advance the simulation according to the current state."""
        if self.state == MENU:
            # gentle idle bobbing on the menu screen
            self.bob_timer += dt
            self.bird.y = settings.SKY_HEIGHT / 2 + math.sin(self.bob_timer * 3.0) * 8.0
            self.bird.update_animation(dt)
            self.bird.rect.center = (int(self.bird.x), int(self.bird.y))
            self.ground.update(dt, settings.BASE_PIPE_SPEED)
        elif self.state == PLAYING:
            speed = settings.pipe_speed_for_score(self.score)
            self.pipes.score = self.score  # difficulty follows the score
            self.pipes.update(dt, speed, settings.spawn_interval_for_score(self.score))
            self.bird.update(dt)
            gained = self.pipes.update_score(settings.BIRD_X)
            if gained:
                self.score += gained
                sounds.play("point")
            self.ground.update(dt, speed)
            bird_rect = self.bird.get_collision_rect()
            if self.ground.collides(bird_rect) or self.pipes.collides(bird_rect):
                self._crash()
        elif self.state == DYING:
            # world freezes; only the bird tumbles down to the ground
            if self.bird.update_dead(dt):
                self._finish()
    # --------------------------------------------------------------- draw
    def draw(self):
        """Render the world and the state-specific UI."""
        self.screen.blit(self.background, (0, 0))
        self.pipes.draw(self.screen)
        self.ground.draw(self.screen)
        self.bird.draw(self.screen)
        if self.state == MENU:
            self.scoreboard.draw_menu(self.screen)
        elif self.state in (PLAYING, DYING):
            self.scoreboard.draw_score(self.screen, self.score)
        elif self.state == GAME_OVER:
            self.scoreboard.draw_game_over(self.screen, self.score, self.new_best)
        pygame.display.flip()