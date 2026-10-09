'''
game.py
The Game class: owns the window, the main loop, the alien formation,
collision handling, scoring, lives and the win/lose conditions.
'''
import random
import pygame
import settings
import ui
from entities import Player, Alien, Bullet, Explosion
class Game:
    """Runs the Space Invaders game loop and holds all game state."""
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT))
        pygame.display.set_caption(settings.TITLE)
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont(None, 28)
        self.big_font = pygame.font.SysFont(None, 72, bold=True)
        self.small_font = pygame.font.SysFont(None, 24)
        self.reset()
    # -- Setup --------------------------------------------------------------
    def reset(self):
        """(Re)initialise all state for a fresh game."""
        self.player = Player()
        self.player_bullets = []
        self.alien_bullets = []
        self.explosions = []
        self.score = 0
        self.state = "playing"          # "playing" | "game_over" | "victory"
        self.direction = 1              # 1 = right, -1 = left
        self.alien_speed = settings.ALIEN_BASE_SPEED
        self.anim_timer_ms = 0
        self.anim_frame = 0
        self._build_formation()
    def _build_formation(self):
        """Create the grid of aliens centred near the top of the screen."""
        self.aliens = []
        grid_w = settings.ALIEN_COLS * settings.ALIEN_WIDTH + (settings.ALIEN_COLS - 1) * settings.ALIEN_H_SPACING
        start_x = (settings.SCREEN_WIDTH - grid_w) / 2
        for row in range(settings.ALIEN_ROWS):
            for col in range(settings.ALIEN_COLS):
                x = start_x + col * (settings.ALIEN_WIDTH + settings.ALIEN_H_SPACING)
                y = settings.ALIEN_TOP_MARGIN + row * (settings.ALIEN_HEIGHT + settings.ALIEN_V_SPACING)
                self.aliens.append(Alien(row, col, x, y))
    # -- Main loop ----------------------------------------------------------
    def run(self):
        """Run until the window is closed."""
        while True:
            dt_ms = self.clock.tick(settings.FPS)
            self._handle_events()
            if self.state == "playing":
                self._update(dt_ms)
            else:
                # Keep explosions animating on the end screens.
                self._update_explosions(dt_ms)
            self._draw()
            pygame.display.flip()
    def _handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self._quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self._quit()
                elif self.state == "playing" and event.key == pygame.K_SPACE:
                    if self.player.can_fire():
                        self.player_bullets.append(self.player.fire())
                elif self.state in ("game_over", "victory") and event.key == pygame.K_r:
                    self.reset()
    @staticmethod
    def _quit():
        pygame.quit()
        raise SystemExit
    # -- Update -------------------------------------------------------------
    def _update(self, dt_ms):
        keys = pygame.key.get_pressed()
        self.player.update(keys, dt_ms)
        self._update_animation(dt_ms)
        self._update_aliens()
        self._alien_fire()
        self._update_bullets(dt_ms)
        self._update_explosions(dt_ms)
        self._handle_collisions()
        self._check_end_conditions()
    ...