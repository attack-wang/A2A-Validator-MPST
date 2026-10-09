'''
Main game class: state management, game loop, drawing.
'''
import random
import sys
import pygame
import settings
from bird import Bird
from pipes import PipeManager
from ground import Ground
from hud import Score, draw_text_with_outline
MENU, PLAYING, GAME_OVER = "menu", "playing", "game_over"
class Game:
    """Main game class: state management, game loop, drawing."""
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((settings.WINDOW_WIDTH, settings.WINDOW_HEIGHT))
        pygame.display.set_caption(settings.WINDOW_TITLE)
        self.clock = pygame.time.Clock()
        self.font_score = pygame.font.SysFont("arial", settings.FONT_SIZE_SCORE, bold=True)
        self.font_text = pygame.font.SysFont("arial", settings.FONT_SIZE_TEXT, bold=True)
        self.font_small = pygame.font.SysFont("arial", settings.FONT_SIZE_SMALL, bold=True)
        self.background = self._make_background()
        self.state = MENU
        self.score = Score()
        self.bird = Bird(settings.BIRD_X, settings.WINDOW_HEIGHT // 2)
        self.pipes = PipeManager()
        self.ground = Ground()
        self.death_flash = 0
        self.frames = 0
    # ------------------------------------------------------------------ setup
    def _make_background(self):
        """Pre-render the static sky gradient and decorative clouds."""
        bg = pygame.Surface((settings.WINDOW_WIDTH, settings.WINDOW_HEIGHT))
        for y in range(settings.WINDOW_HEIGHT):
            t = y / settings.WINDOW_HEIGHT
            color = [int(a + (b - a) * t) for a, b in zip(settings.SKY_TOP, settings.SKY_BOTTOM)]
            pygame.draw.line(bg, color, (0, y), (settings.WINDOW_WIDTH, y))
        # clouds (deterministic so the backdrop looks the same every run)
        rng = random.Random(settings.CLOUD_SEED)
        cloud_color = (240, 250, 252)
        for _ in range(settings.CLOUD_COUNT):
            x = rng.randint(30, settings.WINDOW_WIDTH - 30)
            y = rng.randint(30, settings.WINDOW_HEIGHT // 2)
            scale = rng.uniform(0.8, 1.6)
            self._draw_cloud(bg, x, y, scale, cloud_color)
        return bg
    @staticmethod
    def _draw_cloud(surface, x, y, scale, color):
        """Draw a simple puffy cloud made of overlapping circles."""
        r = int(16 * scale)
        pygame.draw.circle(surface, color, (x, y), r)
        pygame.draw.circle(surface, color, (x + r, y - r // 3), int(r * 0.8))
        pygame.draw.circle(surface, color, (x - r, y - r // 4), int(r * 0.7))
        pygame.draw.circle(surface, color, (x + r // 2, y + r // 3), int(r * 0.7))
        pygame.draw.circle(surface, color, (x - r // 2, y + r // 4), int(r * 0.6))
    # ------------------------------------------------------------- game flow
    def reset_game(self):
        """Return every entity to its starting state."""
        self.bird.reset()
        self.pipes.reset()
        self.score.reset()
        self.ground = Ground()
        self.death_flash = 0
    def start_game(self):
        """Reset the world and begin a new run."""
        self.reset_game()
        self.state = PLAYING
        self.bird.flap()  # give the bird an initial hop
    def game_over(self):
        """Handle the bird dying: persist the best score and flash the screen."""
        self.score.game_over()
        self.death_flash = settings.DEATH_FLASH_FRAMES
        self.state = GAME_OVER
    # --------------------------------------------------------------- events
    def handle_events(self):
        """Process keyboard input and window events."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_SPACE, pygame.K_UP, pygame.K_w):
                    self._handle_flap_key()
                elif event.key == pygame.K_r:
                    if self.state in (PLAYING, GAME_OVER):
                        self.start_game()
                elif event.key == pygame.K_m and self.state == GAME_OVER:
                    self.state = MENU
                    self.reset_game()
                elif event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
    def _handle_flap_key(self):
        if self.state == MENU:
            self.start_game()
        elif self.state == PLAYING:
            self.bird.flap()
        elif self.state == GAME_OVER and self.death_flash <= 0:
            self.start_game()
    # --------------------------------------------------------------- update
    def update(self):
        """Advance the simulation by one frame."""
        self.frames += 1
        if self.death_flash > 0:
            self.death_flash -= 1
        if self.state != PLAYING:
            return
        self.bird.update()
        passed = self.pipes.update(self.score.current, self.bird)
        for _ in range(passed):
            self.score.increment()
        speed = self.pipes.speed_for_score(self.score.current)
        self.ground.update(speed)
        bird_rect = self.bird.get_rect()
        if self.ground.collides(bird_rect) or self.pipes.collides(bird_rect):
            self.bird.alive = False
            self.game_over()
    # ----------------------------------------------------------------- draw
    def draw(self):
        """Render the current frame."""
        self.screen.blit(self.background, (0, 0))
        self.pipes.draw(self.screen)
        self.ground.draw(self.screen)
        self.bird.draw(self.screen)
        if self.state == MENU:
            self._draw_menu()
        else:
            self.score.draw(self.screen, self.font_score)
            if self.state == GAME_OVER:
                self._draw_game_over()
        if self.death_flash > 0:
            flash = pygame.Surface((settings.WINDOW_WIDTH, settings.WINDOW_HEIGHT), pygame.SRCALPHA)
            alpha = int(200 * self.death_flash / settings.DEATH_FLASH_FRAMES)
            flash.fill((255, 255, 255, alpha))
            self.screen.blit(flash, (0, 0))
        pygame.display.flip()
    def _draw_menu(self):
        """Title screen with instructions and the best score."""
        center_x = settings.WINDOW_WIDTH // 2
        draw_text_with_outline(self.screen, "FLAPPY BIRD", self.font_text,
                               (center_x, settings.WINDOW_HEIGHT // 2 - 90),
                               settings.WHITE, settings.SCORE_OUTLINE, 3)
        if self.frames // 30 % 2 == 0:
            draw_text_with_outline(self.screen, "Press SPACE to start", self.font_small,
                                   (center_x, settings.WINDOW_HEIGHT // 2 + 30),
                                   settings.WHITE, settings.SCORE_OUTLINE, 2)
        draw_text_with_outline(self.screen, f"Best: {self.score.best}", self.font_small,
                               (center_x, settings.WINDOW_HEIGHT // 2 + 80),
                               settings.WHITE, settings.SCORE_OUTLINE, 2)
    def _draw_game_over(self):
        """Semi-transparent panel showing the final score."""
        panel_w, panel_h = 280, 170
        panel = pygame.Rect(0, 0, panel_w, panel_h)
        panel.center = (settings.WINDOW_WIDTH // 2, settings.WINDOW_HEIGHT // 2 - 20)
        pygame.draw.rect(self.screen, settings.PANEL_COLOR, panel, border_radius=12)
        pygame.draw.rect(self.screen, settings.PANEL_BORDER, panel, 3, border_radius=12)
        draw_text_with_outline(self.screen, "GAME OVER", self.font_text,
                               (panel.centerx, panel.top + 30),
                               settings.GAME_OVER_COLOR, settings.SCORE_OUTLINE, 2)
        draw_text_with_outline(self.screen, f"Score: {self.score.current}", self.font_small,
                               (panel.centerx, panel.top + 70),
                               settings.WHITE, settings.SCORE_OUTLINE, 2)
        draw_text_with_outline(self.screen, f"Best: {self.score.best}", self.font_small,
                               (panel.centerx, panel.top + 100),
                               settings.WHITE, settings.SCORE_OUTLINE, 2)
        if self.death_flash <= 0 and self.frames // 30 % 2 == 0:
            draw_text_with_outline(self.screen, "Press SPACE or R to restart",
                                   self.font_small,
                                   (panel.centerx, panel.bottom - 25),
                                   settings.WHITE, settings.SCORE_OUTLINE, 2)
    # ------------------------------------------------------------------ run
    def run(self):
        """Main game loop."""
        while True:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(settings.FPS)